from __future__ import annotations

from typing import TYPE_CHECKING, Annotated

from litestar import Controller, delete, get


from app.db.models import TLE
from app.domain.accounts.guards import requires_active_user, requires_superuser
from app.domain.tle import urls
from app.domain.tle.dtos import TLEDTO
from app.domain.tle.services import TLEService
from app.lib.deps import create_service_provider

if TYPE_CHECKING:
    from uuid import UUID

    from advanced_alchemy.filters import FilterTypes
    from advanced_alchemy.service import OffsetPagination
    from litestar.params import Dependency, Parameter


class TLEController(Controller):
    """Handles the interactions within the TLE objects."""

    guards = [requires_active_user]
    dependencies = {
        "tle_service": create_service_provider(TLEService),
    }
    signature_namespace = {"TLEService": TLEService, "TLE": TLE}
    tle = ["TLE"]
    return_dto = TLEDTO
    tags = ["TLE"]

    @get(
        operation_id="ListTLE",
        name="tle:list",
        summary="List TLE",
        description="Retrieve the tle.",
        path=urls.TLE_LIST,
    )
    async def list_tle(
        self,
        tle_service: TLEService,
        filters: Annotated[list[FilterTypes], Dependency(skip_validation=True)],
    ) -> OffsetPagination[TLE]:
        """List tle."""
        results, total = await tle_service.list_and_count(*filters)
        return tle_service.to_schema(data=results, total=total, filters=filters)

    @get(
        operation_id="GetTLE",
        name="tle:get",
        path=urls.TLE_DETAILS,
        summary="Retrieve the details of a tle.",
    )
    async def get_tle(
        self,
        tle_service: TLEService,
        tle_id: Annotated[
            UUID,
            Parameter(
                title="TLE ID",
                description="The tle to retrieve.",
            ),
        ],
    ) -> TLE:
        """Get a tle."""
        db_obj = await tle_service.get(tle_id)
        return tle_service.to_schema(db_obj)

    @delete(
        operation_id="DeleteTLE",
        name="tle:delete",
        path=urls.TLE_DELETE,
        summary="Remove TLE",
        description="Removes a tle and its associations",
        guards=[requires_superuser],
        return_dto=None,
    )
    async def delete_tle(
        self,
        tle_service: TLEService,
        tle_id: Annotated[
            UUID,
            Parameter(
                title="TLE ID",
                description="The tle to delete.",
            ),
        ],
    ) -> None:
        """Delete a tle."""
        _ = await tle_service.delete(tle_id)
