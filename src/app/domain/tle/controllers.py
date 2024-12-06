from litestar import Controller, post
from litestar.di import Provide

from app.domain.satellite.dependencies import provide_satellite_repo
from app.domain.satellite.services import SatelliteRepository
from app.domain.tle.dtos import TLE_Gen, generate_input
from app.lib.geneos import run_program

DETAIL_ROUTE = "/{satellite_id:uuid}"


# TLEgen can be done better with a worker as well?
class TleController(Controller):
    path = "/tle"
    dependencies = {"satellite_repo": Provide(provide_satellite_repo)}
    tags = ["TLE"]

    @post(
        summary="Fit a tle",
        description="Fit two-line elements for a given orbit.",
    )
    async def fit_tle(self, satellite_repo: SatelliteRepository, data: TLE_Gen) -> TLE_Gen:
        satellite = await satellite_repo.get(data.satellite)

        run_program("tleGen", generate_input(data, satellite))

        return data
