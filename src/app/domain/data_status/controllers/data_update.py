from advanced_alchemy.extensions.litestar.dto import SQLAlchemyDTO
from litestar import Controller, post
from litestar.response import Response
from litestar.status_codes import HTTP_202_ACCEPTED

from app.db.models import DataStatus
from app.domain.accounts.guards import requires_superuser
from app.domain.data_status import urls
from app.domain.data_status.services import DataStatusService
from app.domain.data_status.tasks import update_specific_file
from app.lib import dto
from app.lib.deps import create_service_provider


class DataStatusCreateDTO(SQLAlchemyDTO[DataStatus]):
    config = dto.config(exclude={"id", "created_at", "updated_at"})


class DataUpdateController(Controller):
    """Controller for manual data updates."""

    dependencies = {"data_status_service": create_service_provider(DataStatusService)}
    tags = ["Environment Files"]

    @post(
        operation_id="CreateDataUpdate",
        name="data_update:create",
        path=urls.DATA_UPDATE_CREATE,
        summary="Manually update a specific data file",
        guards=[requires_superuser],
    )
    async def update_data(self, data_id: int) -> Response:
        """Trigger update for a specific data file."""
        await update_specific_file(data_id)
        return Response(
            status_code=HTTP_202_ACCEPTED,
            content={"message": f"Update triggered for file ID: {data_id}"},
        )
