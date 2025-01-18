"""Application Modules."""

from __future__ import annotations

from typing import TYPE_CHECKING

from app.domain.accounts.controllers import AccessController, UserController, UserRoleController
from app.domain.data_status.controllers.data_status import DataStatusController
from app.domain.data_status.controllers.data_update import DataUpdateController
from app.domain.dynamics.controllers import DynamicsController
from app.domain.ground_station.controllers import GroundStationController
from app.domain.orbit.controllers import OrbitController
from app.domain.propagation.controllers import PropagationController
from app.domain.satellite.controllers import SatelliteController
from app.domain.system.controllers import SystemController
from app.domain.tags.controllers import TagController
from app.domain.teams.controllers import TeamController, TeamMemberController
from app.domain.tle.controllers.tle_fitting import TleFitController
from app.domain.tle.controllers.tles import TLEController
from app.domain.util.controllers.state_conversion import ConversionController
from app.domain.web.controllers import WebController

if TYPE_CHECKING:
    from litestar.types import ControllerRouterHandler


route_handlers: list[ControllerRouterHandler] = [
    AccessController,
    UserController,
    TeamController,
    UserRoleController,
    #  TeamInvitationController,
    TeamMemberController,
    TagController,
    SystemController,
    WebController,
    DataStatusController,
    DataUpdateController,
    GroundStationController,
    SatelliteController,
    DynamicsController,
    PropagationController,
    OrbitController,
    TLEController,
    TleFitController,
    ConversionController,
]
