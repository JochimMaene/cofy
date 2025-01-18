import asyncio
from datetime import UTC, datetime

import httpx
from croniter import croniter
from litestar.status_codes import HTTP_200_OK
from saq.types import Context
from structlog import get_logger

from app.config.app import alchemy
from app.db.models.data_status import DataStatus, StatusType
from app.domain.data_status.dependencies import provide_data_status_service
from app.domain.data_status.services import DataStatusService
from app.domain.data_status.settings import ENVIRONMENT_DATA_SETTINGS, EnvironementDataUpdateSettings

logger = get_logger()


async def _update_data_file(
    data_setting: EnvironementDataUpdateSettings,
    data_status: DataStatus | None,
    service: DataStatusService,
    client: httpx.AsyncClient,
    file_id: int,
) -> None:
    """Common logic for updating a data file."""

    response = await client.get(data_setting.URL, timeout=30)

    if response.status_code == HTTP_200_OK:
        data_setting.update_func(response, data_setting.file_name)
        status = StatusType.updated
    else:
        status = StatusType.out_of_date
        if data_status:
            await logger.warning("File for %s couldn't be updated. Using old one.", data_setting.name)

    current_time = datetime.now(UTC)
    next_update = croniter(data_setting.cron, current_time).get_next(datetime) if data_setting.cron else None

    updated_status = DataStatus(
        id=file_id,
        name=data_setting.name if not data_status else data_status.name,
        last_update=current_time,
        next_update=next_update,
        status=status,
        URL=data_setting.URL if not data_status else data_status.URL,
        cron=data_setting.cron if not data_status else data_status.cron,
    )

    if data_status:
        await service.update(updated_status, auto_commit=True)
    else:
        await service.create(updated_status, auto_commit=True)


async def update_environment_files_status(_: Context) -> None:
    await logger.ainfo("Checking environment files status.")
    client = httpx.AsyncClient(verify=False)

    try:
        async with alchemy.get_session() as db_session:
            service = await anext(provide_data_status_service(db_session))

            update_tasks = []
            for key, data_setting in ENVIRONMENT_DATA_SETTINGS.items():
                data_status = await service.get(key) if await service.exists(id=key) else None
                if not data_status or (data_status.cron and datetime.now(UTC) > data_status.next_update):
                    await logger.ainfo(f"Queuing {data_setting.name} file update.")
                    update_tasks.append(_update_data_file(data_setting, data_status, service, client, key))

            if update_tasks:
                await asyncio.gather(*update_tasks)
    finally:
        await client.aclose()


async def update_specific_file(file_id: int) -> None:
    await logger.ainfo(f"Manual update triggered for file ID: {file_id}")
    client = httpx.AsyncClient(verify=False)

    try:
        async with alchemy.get_session() as db_session:
            service = await anext(provide_data_status_service(db_session))
            data_status = await service.get(file_id)

            if not data_status:
                await logger.error("No data status found for ID: %s", file_id)
                return

            data_setting = ENVIRONMENT_DATA_SETTINGS.get(file_id)
            if not data_setting:
                await logger.error("No data setting found for ID: %s", file_id)
                return

            await _update_data_file(data_setting, data_status, service, client, file_id)
    finally:
        await client.aclose()
