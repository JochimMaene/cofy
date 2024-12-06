from __future__ import annotations

from typing import TYPE_CHECKING, Annotated

from litestar import Controller, delete, get, patch, post
from litestar.di import Provide

from app.db.models import Satellite
from app.domain.accounts.guards import requires_active_user, requires_superuser
from app.domain.satellite import urls
from app.domain.satellite.dependencies import provide_satellite_service
from app.domain.satellite.dtos import SatelliteCreateDTO, SatelliteDTO, SatelliteUpdateDTO
from app.domain.satellite.services import SatelliteService

if TYPE_CHECKING:
    from uuid import UUID

    from advanced_alchemy.filters import FilterTypes
    from advanced_alchemy.service import OffsetPagination
    from litestar.dto import DTOData
    from litestar.params import Dependency, Parameter


class SatelliteController(Controller):
    """Handles the interactions within the Satellite objects."""

    guards = [requires_active_user]
    dependencies = {"satellite_service": Provide(provide_satellite_service)}
    signature_namespace = {"SatelliteService": SatelliteService, "Satellite": Satellite}
    satellite = ["Satellite"]
    return_dto = SatelliteDTO
    tags = ["Satellite"]

    @get(
        operation_id="ListSatellite",
        name="satellite:list",
        summary="List Satellite",
        description="Retrieve the satellite.",
        path=urls.TAG_LIST,
    )
    async def list_satellite(
        self,
        satellite_service: SatelliteService,
        filters: Annotated[list[FilterTypes], Dependency(skip_validation=True)],
    ) -> OffsetPagination[Satellite]:
        """List satellite."""
        results, total = await satellite_service.list_and_count(*filters)
        return satellite_service.to_schema(data=results, total=total, filters=filters)

    @get(
        operation_id="GetSatellite",
        name="satellite:get",
        path=urls.TAG_DETAILS,
        summary="Retrieve the details of a satellite.",
    )
    async def get_satellite(
        self,
        satellite_service: SatelliteService,
        satellite_id: Annotated[
            UUID,
            Parameter(
                title="Satellite ID",
                description="The satellite to retrieve.",
            ),
        ],
    ) -> Satellite:
        """Get a satellite."""
        db_obj = await satellite_service.get(satellite_id)
        return satellite_service.to_schema(db_obj)

    @post(
        operation_id="CreateSatellite",
        name="satellite:create",
        summary="Create a new satellite.",
        cache_control=None,
        description="A satellite is a place where you can upload and group collections of databases.",
        guards=[requires_superuser],
        path=urls.TAG_CREATE,
        dto=SatelliteCreateDTO,
    )
    async def create_satellite(
        self,
        satellite_service: SatelliteService,
        data: DTOData[Satellite],
    ) -> Satellite:
        """Create a new satellite."""
        db_obj = await satellite_service.create(data.create_instance())
        return satellite_service.to_schema(db_obj)

    @patch(
        operation_id="UpdateSatellite",
        name="satellite:update",
        path=urls.TAG_UPDATE,
        guards=[requires_superuser],
        dto=SatelliteUpdateDTO,
    )
    async def update_satellite(
        self,
        satellite_service: SatelliteService,
        data: DTOData[Satellite],
        satellite_id: Annotated[
            UUID,
            Parameter(
                title="Satellite ID",
                description="The satellite to update.",
            ),
        ],
    ) -> Satellite:
        """Update a satellite."""
        db_obj = await satellite_service.update(item_id=satellite_id, data=data.create_instance())
        return satellite_service.to_schema(db_obj)

    @delete(
        operation_id="DeleteSatellite",
        name="satellite:delete",
        path=urls.TAG_DELETE,
        summary="Remove Satellite",
        description="Removes a satellite and its associations",
        guards=[requires_superuser],
        return_dto=None,
    )
    async def delete_satellite(
        self,
        satellite_service: SatelliteService,
        satellite_id: Annotated[
            UUID,
            Parameter(
                title="Satellite ID",
                description="The satellite to delete.",
            ),
        ],
    ) -> None:
        """Delete a satellite."""
        _ = await satellite_service.delete(satellite_id)
