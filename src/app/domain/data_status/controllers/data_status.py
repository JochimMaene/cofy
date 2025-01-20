from collections.abc import Sequence

from advanced_alchemy.extensions.litestar.dto import SQLAlchemyDTO
from litestar import Controller, get, patch
from litestar.dto import DTOData

from app.db.models import DataStatus
from app.domain.accounts.guards import requires_active_user, requires_superuser
from app.domain.data_status import urls
from app.domain.data_status.services import DataStatusService
from app.lib import dto
from app.lib.deps import create_service_provider

__all__ = ["DataStatusController"]

class DataStatusDTO(SQLAlchemyDTO[DataStatus]):
    config = dto.config(exclude={"created_at", "updated_at"})


class DataStatusUpdateDTO(SQLAlchemyDTO[DataStatus]):
    config = dto.config(exclude={"id", "created_at", "updated_at"}, partial=True)


class DataStatusController(Controller):
    """Handles the interactions within the Tag objects."""

    guards = [requires_active_user]
    dependencies = {"data_status_service": create_service_provider(DataStatusService)}
    signature_types = [DataStatusService]
    tags = ["Environment Files"]
    return_dto = DataStatusDTO

    @get(
        operation_id="ListDataStatus",
        name="data_status:list",
        summary="List the environment data status",
        description="List all statuses of the environment files.",
        path=urls.DATA_STATUS_LIST,
    )
    async def list_data_status(
        self,
        data_status_service: DataStatusService,
    ) -> Sequence[DataStatus]:
        return await data_status_service.list()

    @get(
        operation_id="GetDataStatus",
        name="data_status:details",
        summary="Get a specific environment data status",
        description="Get a the status of a specific environment data file from the database using the unique id.",
        path=urls.DATA_STATUS_DETAILS,
    )
    async def get_data_status(self, data_status_service: DataStatusService, data_id: int) -> DataStatus:
        return await data_status_service.get(data_id)

    @patch(
        summary="Update a specific specific environment data setting",
        description="Update a setting of how the environment data file is updated.",
        path=urls.DATA_STATUS_UPDATE,
        guards=[requires_superuser],
        dto=DataStatusUpdateDTO,
    )
    async def update_data_status(
        self,
        data: DTOData[DataStatus],
        data_status_service: DataStatusService,
        data_id: int,
    ) -> DataStatus:
        return await data_status_service.update(DataStatus(id=data_id, **data.as_builtins()))
