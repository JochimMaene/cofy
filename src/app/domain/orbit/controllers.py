from __future__ import annotations

from typing import TYPE_CHECKING, Annotated

from litestar import Controller, delete, get, patch, post
from litestar.di import Provide

from app.db.models import Orbit
from app.domain.accounts.guards import requires_active_user, requires_superuser
from app.domain.orbit import urls
from app.domain.orbit.dependencies import provide_orbit_service
from app.domain.orbit.dtos import OrbitCreateDTO, OrbitDTO, OrbitUpdateDTO
from app.domain.orbit.services import OrbitService

if TYPE_CHECKING:
    from uuid import UUID

    from advanced_alchemy.filters import FilterTypes
    from advanced_alchemy.service import OffsetPagination
    from litestar.dto import DTOData
    from litestar.params import Dependency, Parameter


class OrbitController(Controller):
    """Handles the interactions within the Orbit objects."""

    guards = [requires_active_user]
    dependencies = {"orbit_service": Provide(provide_orbit_service)}
    signature_namespace = {"OrbitService": OrbitService, "Orbit": Orbit}
    orbit = ["Orbit"]
    return_dto = OrbitDTO
    tags = ["Orbit"]

    @get(
        operation_id="ListOrbit",
        name="orbit:list",
        summary="List Orbit",
        description="Retrieve the orbit.",
        path=urls.TAG_LIST,
    )
    async def list_orbit(
        self,
        orbit_service: OrbitService,
        filters: Annotated[list[FilterTypes], Dependency(skip_validation=True)],
    ) -> OffsetPagination[Orbit]:
        """List orbit."""
        results, total = await orbit_service.list_and_count(*filters)
        return orbit_service.to_schema(data=results, total=total, filters=filters)

    @get(
        operation_id="GetOrbit",
        name="orbit:get",
        path=urls.TAG_DETAILS,
        summary="Retrieve the details of a orbit.",
    )
    async def get_orbit(
        self,
        orbit_service: OrbitService,
        orbit_id: Annotated[
            UUID,
            Parameter(
                title="Orbit ID",
                description="The orbit to retrieve.",
            ),
        ],
    ) -> Orbit:
        """Get a orbit."""
        db_obj = await orbit_service.get(orbit_id)
        return orbit_service.to_schema(db_obj)

    @post(
        operation_id="CreateOrbit",
        name="orbit:create",
        summary="Create a new orbit.",
        cache_control=None,
        description="A orbit is a place where you can upload and group collections of databases.",
        guards=[requires_superuser],
        path=urls.TAG_CREATE,
        dto=OrbitCreateDTO,
    )
    async def create_orbit(
        self,
        orbit_service: OrbitService,
        data: DTOData[Orbit],
    ) -> Orbit:
        """Create a new orbit."""
        db_obj = await orbit_service.create(data.create_instance())
        return orbit_service.to_schema(db_obj)

    @patch(
        operation_id="UpdateOrbit",
        name="orbit:update",
        path=urls.TAG_UPDATE,
        guards=[requires_superuser],
        dto=OrbitUpdateDTO,
    )
    async def update_orbit(
        self,
        orbit_service: OrbitService,
        data: DTOData[Orbit],
        orbit_id: Annotated[
            UUID,
            Parameter(
                title="Orbit ID",
                description="The orbit to update.",
            ),
        ],
    ) -> Orbit:
        """Update a orbit."""
        db_obj = await orbit_service.update(item_id=orbit_id, data=data.create_instance())
        return orbit_service.to_schema(db_obj)

    @delete(
        operation_id="DeleteOrbit",
        name="orbit:delete",
        path=urls.TAG_DELETE,
        summary="Remove Orbit",
        description="Removes a orbit and its associations",
        guards=[requires_superuser],
        return_dto=None,
    )
    async def delete_orbit(
        self,
        orbit_service: OrbitService,
        orbit_id: Annotated[
            UUID,
            Parameter(
                title="Orbit ID",
                description="The orbit to delete.",
            ),
        ],
    ) -> None:
        """Delete a orbit."""
        _ = await orbit_service.delete(orbit_id)
