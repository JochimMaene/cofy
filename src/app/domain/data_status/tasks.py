from datetime import UTC, datetime

import httpx
from croniter import croniter
from litestar.status_codes import HTTP_200_OK
from saq.types import Context
from structlog import get_logger

from app.config.app import alchemy
from app.db.models.data_status import DataStatus, StatusType
from app.domain.data_status.dependencies import provide_data_status_service
from app.domain.data_status.settings import ENVIRONMENT_DATA_SETTINGS

logger = get_logger()


# could be better to get rid of async here
async def update_environment_files_status(_: Context) -> None:
    await logger.ainfo("Checking environment files status.")
    client = httpx.AsyncClient(verify=False)
    async with alchemy.get_session() as db_session:
        service = await anext(provide_data_status_service(db_session))

        for key, data_setting in ENVIRONMENT_DATA_SETTINGS.items():
            data_status_exists = await service.exists(id=key)

            if not data_status_exists:
                await logger.ainfo(f"Performing {data_setting.name} file update because the status is not known.")
                response = await client.get(data_setting.URL)
                if response.status_code == HTTP_200_OK:
                    data_setting.update_func(response, data_setting.file_name)
                    status = StatusType.updated
                else:
                    status = StatusType.out_of_date
                current_time = datetime.now(UTC)
                if data_setting.cron is not None:
                    next_update = croniter(data_setting.cron, current_time).get_next(datetime)
                else:
                    next_update = None
                data_status = DataStatus(
                    id=key,
                    name=data_setting.name,
                    last_update=current_time,
                    next_update=next_update,
                    status=status,
                    URL=data_setting.URL,
                    cron=data_setting.cron,
                )
                await service.create(data_status, auto_commit=True)

            else:
                data_status = await service.get(key)
                current_time = datetime.now(UTC)
                if data_status.cron is not None and current_time > data_status.next_update:
                    await logger.ainfo(f"Performing {data_status.name} file update as it is out-of-date.")
                    response = await client.get(data_status.URL)
                    next_update = croniter(data_status.cron, current_time).get_next(datetime)
                    if response.status_code == HTTP_200_OK:
                        data_setting.update_func(response, data_setting.file_name)
                        data_status = DataStatus(
                            id=key,
                            last_update=current_time,
                            next_update=next_update,
                            status=StatusType.updated,
                        )

                        await service.update(data_status, auto_commit=True)
                    else:
                        await logger.warning("File for %s couldn't be updated. Using old one.", data_status.name)
                        data_status = DataStatus(
                            id=key,
                            next_update=next_update,
                            status=StatusType.out_of_date,
                        )
                        await service.update(data_status, auto_commit=True)

    await client.aclose()
