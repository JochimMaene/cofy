from __future__ import annotations

from typing import TYPE_CHECKING, Annotated

from litestar import Controller, delete, get, patch, post
from litestar.di import Provide

from app.db.models import Dynamics
from app.domain.accounts.guards import requires_active_user, requires_superuser
from app.domain.dynamics import urls
from app.domain.dynamics.dependencies import provide_dynamics_service
from app.domain.dynamics.dtos import DynamicsCreateDTO, DynamicsDTO, DynamicsUpdateDTO
from app.domain.dynamics.services import DynamicsService

if TYPE_CHECKING:
    from uuid import UUID

    from advanced_alchemy.filters import FilterTypes
    from advanced_alchemy.service import OffsetPagination
    from litestar.dto import DTOData
    from litestar.params import Dependency, Parameter


class DynamicsController(Controller):
    """Handles the interactions within the Dynamics objects."""

    guards = [requires_active_user]
    dependencies = {"dynamics_service": Provide(provide_dynamics_service)}
    signature_namespace = {"DynamicsService": DynamicsService, "Dynamics": Dynamics}
    dynamics = ["Dynamics"]
    return_dto = DynamicsDTO
    tags = ["Dynamics"]

    @get(
        operation_id="ListDynamics",
        name="dynamics:list",
        summary="List Dynamics",
        description="Retrieve the dynamics.",
        path=urls.TAG_LIST,
    )
    async def list_dynamics(
        self,
        dynamics_service: DynamicsService,
        filters: Annotated[list[FilterTypes], Dependency(skip_validation=True)],
    ) -> OffsetPagination[Dynamics]:
        """List dynamics."""
        results, total = await dynamics_service.list_and_count(*filters)
        return dynamics_service.to_schema(data=results, total=total, filters=filters)

    @get(
        operation_id="GetDynamics",
        name="dynamics:get",
        path=urls.TAG_DETAILS,
        summary="Retrieve the details of a dynamics.",
    )
    async def get_dynamics(
        self,
        dynamics_service: DynamicsService,
        dynamics_id: Annotated[
            UUID,
            Parameter(
                title="Dynamics ID",
                description="The dynamics to retrieve.",
            ),
        ],
    ) -> Dynamics:
        """Get a dynamics."""
        db_obj = await dynamics_service.get(dynamics_id)
        return dynamics_service.to_schema(db_obj)

    @post(
        operation_id="CreateDynamics",
        name="dynamics:create",
        summary="Create a new dynamics.",
        cache_control=None,
        description="A dynamics is a place where you can upload and group collections of databases.",
        guards=[requires_superuser],
        path=urls.TAG_CREATE,
        dto=DynamicsCreateDTO,
    )
    async def create_dynamics(
        self,
        dynamics_service: DynamicsService,
        data: DTOData[Dynamics],
    ) -> Dynamics:
        """Create a new dynamics."""
        db_obj = await dynamics_service.create(data.create_instance())
        return dynamics_service.to_schema(db_obj)

    @patch(
        operation_id="UpdateDynamics",
        name="dynamics:update",
        path=urls.TAG_UPDATE,
        guards=[requires_superuser],
        dto=DynamicsUpdateDTO,
    )
    async def update_dynamics(
        self,
        dynamics_service: DynamicsService,
        data: DTOData[Dynamics],
        dynamics_id: Annotated[
            UUID,
            Parameter(
                title="Dynamics ID",
                description="The dynamics to update.",
            ),
        ],
    ) -> Dynamics:
        """Update a dynamics."""
        db_obj = await dynamics_service.update(item_id=dynamics_id, data=data.create_instance())
        return dynamics_service.to_schema(db_obj)

    @delete(
        operation_id="DeleteDynamics",
        name="dynamics:delete",
        path=urls.TAG_DELETE,
        summary="Remove Dynamics",
        description="Removes a dynamics and its associations",
        guards=[requires_superuser],
        return_dto=None,
    )
    async def delete_dynamics(
        self,
        dynamics_service: DynamicsService,
        dynamics_id: Annotated[
            UUID,
            Parameter(
                title="Dynamics ID",
                description="The dynamics to delete.",
            ),
        ],
    ) -> None:
        """Delete a dynamics."""
        _ = await dynamics_service.delete(dynamics_id)
