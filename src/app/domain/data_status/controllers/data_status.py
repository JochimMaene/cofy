from collections.abc import Sequence

from litestar import Controller, get, patch
from litestar.di import Provide
from litestar.dto import DTOData

from app.db.models.data_status import DataStatus
from app.domain.accounts.guards import requires_active_user, requires_superuser
from app.domain.data_status import urls
from app.domain.data_status.dependencies import provide_data_status_service
from app.domain.data_status.dtos import DataStatusDTO, DataStatusUpdateDTO
from app.domain.data_status.services import DataStatusService

__all__ = ["DataStatusController"]


class DataStatusController(Controller):
    """Handles the interactions within the Tag objects."""

    guards = [requires_active_user]
    dependencies = {"data_status_service": Provide(provide_data_status_service)}
    signature_namespace = {"DataStatusService": DataStatusService, "DataStatus": DataStatus}
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
