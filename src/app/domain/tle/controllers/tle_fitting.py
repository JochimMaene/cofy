from datetime import datetime

from godot.core.tempo import Epoch
from litestar import post
from litestar.controller import Controller
from litestar.di import Provide
from litestar.dto import MsgspecDTO

from app.db.models import TLE
from app.domain.accounts.guards import requires_active_user
from app.domain.orbit.dependencies import provide_orbit_service
from app.domain.orbit.services import OrbitService
from app.domain.tle import urls
from app.domain.tle.dependencies import provide_tle_service
from app.domain.tle.dtos import TLEDTO
from app.domain.tle.schemas import TleGenerationFromOrbitInput
from app.domain.tle.services import TLEService
from app.domain.tle.tasks import fit_tle_from_orbit


def convert_godot_epoch_to_datetime(godot_epoch: Epoch) -> datetime:
    return datetime.fromisoformat(godot_epoch.calStr("UTC")[:-4] + "Z")


class TleFitController(Controller):
    dependencies = {
        "tle_service": Provide(provide_tle_service),
        "orbit_service": Provide(provide_orbit_service),
    }
    tags = ["TLE"]

    @post(
        operation_id="CreateTleFitRequest",
        name="tle:fit",
        summary="Request TLE fit",
        description="Fit a TLE through a numerically propagated orbit.",
        guards=[requires_active_user],
        path=urls.TLE_FIT,
        dto=MsgspecDTO[TleGenerationFromOrbitInput],
        return_dto=TLEDTO,
    )
    async def create_propagation_request(
        self,
        orbit_service: OrbitService,
        tle_service: TLEService,
        data: TleGenerationFromOrbitInput,
    ) -> TLE:
        orbit = await orbit_service.get(data.orbit_id)

        [epoch, line1, line2] = fit_tle_from_orbit(orbit, data.step)

        db_obj = await tle_service.create(
            TLE(
                line1=line1,
                line2=line2,
                epoch=convert_godot_epoch_to_datetime(epoch),
                originator="internal",
                satellite_id=orbit.satellite.id,
            ),
        )
        return tle_service.to_schema(db_obj)
