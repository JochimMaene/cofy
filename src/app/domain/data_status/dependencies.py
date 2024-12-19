from __future__ import annotations

from typing import TYPE_CHECKING

from app.domain.data_status.services import DataStatusService

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from sqlalchemy.ext.asyncio import AsyncSession

__all__ = ["provide_data_status_service"]


async def provide_data_status_service(
    db_session: AsyncSession | None = None,
) -> AsyncGenerator[DataStatusService, None]:
    async with DataStatusService.new(
        session=db_session,
    ) as service:
        yield service
