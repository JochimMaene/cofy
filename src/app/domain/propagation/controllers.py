import datetime
from tempfile import NamedTemporaryFile
from typing import Any
from uuid import UUID, uuid4

from godot import cosmos
from godot.core import ipfwrap
from godot.core.tempo import Epoch
from litestar import post
from litestar.controller import Controller
from litestar.datastructures import UploadFile
from litestar.di import Provide
from litestar.dto import MsgspecDTO
from litestar_saq.config import TaskQueues
from structlog import get_logger

from app.config.app import alchemy
from app.domain.accounts.guards import requires_active_user
from app.domain.orbit.services import OrbitService
from app.domain.propagation import urls
from app.domain.propagation.schemas import JobRequest, PropagationInput, PropagationResult, return_propagation_template
from app.domain.satellite.dependencies import provide_satellite_service
from app.domain.satellite.services import SatelliteService
from app.lib.exceptions import ApplicationClientError
from app.lib.fdy import get_dynamics_config
from app.lib.storage_service import FileStorageService
from app.lib.universe_assembler import uni_config as uni_basic

logger = get_logger()


def convert_godot_epoch_to_datetime(godot_epoch: Epoch) -> datetime.datetime:
    return datetime.datetime.fromisoformat(godot_epoch.calStr("UTC")[:-4] + "Z")


# simple file data store for now
async def propagate_and_save(
    ctx: Any,
    *,
    tra_config: dict,
    uni_config: dict,
) -> None:
    try:
        uni = cosmos.Universe(uni_config)
        tra = cosmos.Trajectory(uni, tra_config)
        tra.compute(False)

    except Exception:
        logger.exception("An error occurred during propagation.")
        raise
    # with tempfile.NamedTemporaryFile() as f:
    # id of the Earth as center of the ephemerides, according to the IMSORB body identification scheme
    earth_id = 3

    file_header = [0, earth_id, 1, 0, 0, 0, 0, 0]
    with NamedTemporaryFile() as f:
        ipf_writer = ipfwrap.IpfWriter(
            f.name,
            dimension=6,  # 6 state elements (position and velocity)
            derivatives=0,  # the ephemerides don't provide derivatives
            fileType=1,  # indicates that this is an orbit interpolation file
            blockHeaderSize=2,  # required block size for orbit interpolation files
            fileHeader=file_header,
        )
        cosmos.writeIpf(ipf_writer, uni, tra, tra_config["setup"][0]["name"] + "_center", "ICRF", {"Earth": earth_id})
        del ipf_writer
        file_name = str(uuid4()) + ".ipf"

        async with FileStorageService.new(
            uploads_dir="data/uploads",
            allow_extensions=["ipf"],
        ) as file_storage_service:
            up_file = UploadFile("bytes", file_name, f.read())
            await file_storage_service.upload([up_file])

        async with (
            alchemy.get_session() as db_session,
            OrbitService.new(
                session=db_session,
            ) as orbit_service,
        ):
            _ = await orbit_service.create(
                data={
                    "file_name": file_name,
                    "start": convert_godot_epoch_to_datetime(Epoch(tra_config["timeline"][0]["epoch"])),
                    "end": convert_godot_epoch_to_datetime(Epoch(tra_config["timeline"][1]["point"]["epoch"])),
                    "satellite_id": str(UUID(hex=tra_config["setup"][0]["name"])),
                },
                auto_commit=True,
                auto_refresh=True,
            )


class PropagationController(Controller):
    guards = [requires_active_user]
    dependencies = {
        "satellite_service": Provide(provide_satellite_service),
    }
    tags = ["Propagation"]

    @post(
        operation_id="CreatePropagationRequest",
        name="propagate:request",
        summary="Request numerical orbit propagation",
        description="Submit an orbit propagation request using the numerical GODOT orbit propagator.\
              The result will be saved as a .ipf file.",
        guards=[requires_active_user],
        path=urls.PROPAGATION_REQUEST,
        dto=MsgspecDTO[PropagationInput],
        return_dto=MsgspecDTO[PropagationResult],
    )
    async def create_propagation_request(
        self,
        satellite_service: SatelliteService,
        # file_storage_service: FileStorageService,
        data: PropagationInput,
        task_queues: TaskQueues,
    ) -> JobRequest:
        satellite = await satellite_service.get(data.satellite_id)

        uni_config = uni_basic | get_dynamics_config(satellite.dynamics, satellite)

        tra_config = return_propagation_template(data)

        queue = task_queues.get("Orbit propagation queue")
        job = await queue.enqueue(
            "propagate_and_save",
            tra_config=tra_config,
            uni_config=uni_config,
        )

        if job is None:
            msg = "Failed to enqueue the propagation job."
            raise ApplicationClientError(msg)

        return JobRequest(queue_id=UUID(job.key), location=f"saq/api/queues/{job.id}")
