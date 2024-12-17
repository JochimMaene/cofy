from __future__ import annotations

from typing import TYPE_CHECKING, Annotated

from litestar import Controller, delete, get, patch, post
from litestar.di import Provide

from app.db.models import GroundStation
from app.domain.accounts.guards import requires_active_user, requires_superuser
from app.domain.ground_station import urls
from app.domain.ground_station.dependencies import provide_ground_station_service
from app.domain.ground_station.dtos import GroundStationCreateDTO, GroundStationDTO, GroundStationUpdateDTO
from app.domain.ground_station.services import GroundStationService

if TYPE_CHECKING:
    from uuid import UUID

    from advanced_alchemy.filters import FilterTypes
    from advanced_alchemy.service import OffsetPagination
    from litestar.dto import DTOData
    from litestar.params import Dependency, Parameter


class GroundStationController(Controller):
    """Handles the interactions within the GroundStation objects."""

    guards = [requires_active_user]
    dependencies = {"ground_station_service": Provide(provide_ground_station_service)}
    signature_namespace = {"GroundStationService": GroundStationService, "GroundStation": GroundStation}
    ground_station = ["GroundStation"]
    return_dto = GroundStationDTO
    tags = ["Ground Stations"]

    @get(
        operation_id="ListGroundStation",
        name="ground_station:list",
        summary="List GroundStation",
        description="Retrieve the ground_station.",
        path=urls.GROUND_STATION_LIST,
    )
    async def list_ground_station(
        self,
        ground_station_service: GroundStationService,
        filters: Annotated[list[FilterTypes], Dependency(skip_validation=True)],
    ) -> OffsetPagination[GroundStation]:
        """List ground_station."""
        results, total = await ground_station_service.list_and_count(*filters)
        return ground_station_service.to_schema(data=results, total=total, filters=filters)

    @get(
        operation_id="GetGroundStation",
        name="ground_station:get",
        path=urls.GROUND_STATION_DETAILS,
        summary="Retrieve the details of a ground_station.",
    )
    async def get_ground_station(
        self,
        ground_station_service: GroundStationService,
        ground_station_id: Annotated[
            UUID,
            Parameter(
                title="GroundStation ID",
                description="The ground_station to retrieve.",
            ),
        ],
    ) -> GroundStation:
        """Get a ground_station."""
        db_obj = await ground_station_service.get(ground_station_id)
        return ground_station_service.to_schema(db_obj)

    @post(
        operation_id="CreateGroundStation",
        name="ground_station:create",
        summary="Create a new ground_station.",
        cache_control=None,
        description="A ground_station is a place where you can upload and group collections of databases.",
        guards=[requires_superuser],
        path=urls.GROUND_STATION_CREATE,
        dto=GroundStationCreateDTO,
    )
    async def create_ground_station(
        self,
        ground_station_service: GroundStationService,
        data: DTOData[GroundStation],
    ) -> GroundStation:
        """Create a new ground_station."""
        db_obj = await ground_station_service.create(data.create_instance())
        return ground_station_service.to_schema(db_obj)

    @patch(
        operation_id="UpdateGroundStation",
        name="ground_station:update",
        path=urls.GROUND_STATION_UPDATE,
        guards=[requires_superuser],
        dto=GroundStationUpdateDTO,
    )
    async def update_ground_station(
        self,
        ground_station_service: GroundStationService,
        data: DTOData[GroundStation],
        ground_station_id: Annotated[
            UUID,
            Parameter(
                title="GroundStation ID",
                description="The ground_station to update.",
            ),
        ],
    ) -> GroundStation:
        """Update a ground_station."""
        db_obj = await ground_station_service.update(item_id=ground_station_id, data=data.create_instance())
        return ground_station_service.to_schema(db_obj)

    @delete(
        operation_id="DeleteGroundStation",
        name="ground_station:delete",
        path=urls.GROUND_STATION_DELETE,
        summary="Remove GroundStation",
        description="Removes a ground_station and its associations",
        guards=[requires_superuser],
        return_dto=None,
    )
    async def delete_ground_station(
        self,
        ground_station_service: GroundStationService,
        ground_station_id: Annotated[
            UUID,
            Parameter(
                title="GroundStation ID",
                description="The ground_station to delete.",
            ),
        ],
    ) -> None:
        """Delete a ground_station."""
        _ = await ground_station_service.delete(ground_station_id)
