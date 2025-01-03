from __future__ import annotations

from typing import TYPE_CHECKING

from app.domain.tle.services import TLEService

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from sqlalchemy.ext.asyncio import AsyncSession

__all__ = ["provide_tle_service"]


async def provide_tle_service(
    db_session: AsyncSession | None = None,
) -> AsyncGenerator[TLEService, None]:
    """Provide TLEs service.

    Args:
        db_session (AsyncSession | None, optional): current database session. Defaults to None.

    Returns:
        TLEService: An TLE service object
    """
    async with TLEService.new(
        session=db_session,
    ) as service:
        yield service
