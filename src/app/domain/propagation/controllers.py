from godot import cosmos
from godot.core import ipfwrap
from litestar import post
from litestar.controller import Controller
from litestar.di import Provide
from litestar.dto import MsgspecDTO
from litestar_saq.config import TaskQueues

from app.domain.accounts.guards import requires_active_user
from app.domain.propagation import urls
from app.domain.propagation.schemas import JobRequest, PropagationInput, PropagationResult, return_propagation_template
from app.domain.satellite.dependencies import provide_satellite_service
from app.domain.satellite.services import SatelliteService
from app.lib.fdy import get_dynamics_config
from app.lib.universe_assembler import uni as uni_basic


# simple file data store for now
async def propagate_and_save(ctx, *, tra_config: dict, uni_config: dict) -> None:
    uni = cosmos.Universe(uni_config)
    tra = cosmos.Trajectory(uni, tra_config)
    tra.compute(False)

    # with tempfile.NamedTemporaryFile() as f:
    # id of the Earth as center of the ephemerides, according to the IMSORB body identification scheme
    EARTH_ID = 3

    fileHeader = [0, EARTH_ID, 1, 0, 0, 0, 0, 0]

    ipf_writer = ipfwrap.IpfWriter(
        "data/sample.ipf",
        dimension=6,  # 6 state elements (position and velocity)
        derivatives=0,  # the ephemerides don't provide derivatives
        fileType=1,  # indicates that this is an orbit interpolation file
        blockHeaderSize=2,  # required block size for orbit interpolation files
        fileHeader=fileHeader,
    )
    cosmos.writeIpf(ipf_writer, uni, tra, tra_config["setup"][0]["name"] + "_center", "ICRF", {"Earth": EARTH_ID})


class PropagationController(Controller):
    path = "/propagate/"
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
        data: PropagationInput,
        task_queues: TaskQueues,
    ) -> JobRequest:
        satellite = await satellite_service.get(data.satellite)

        uni_config = uni_basic | get_dynamics_config(satellite.dynamics, satellite)

        tra_config = return_propagation_template(data)

        queue = task_queues.get("Orbit propagation queue")
        job = await queue.enqueue(
            "propagate_and_save",
            tra_config=tra_config,
            uni_config=uni_config,
        )
        return JobRequest(queue_id=job.key, location=f"saq/api/queues/{job.id}")
