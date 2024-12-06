from __future__ import annotations

from typing import TYPE_CHECKING

from app.domain.satellite.services import SatelliteService

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from sqlalchemy.ext.asyncio import AsyncSession

__all__ = ["provide_satellite_service"]


async def provide_satellite_service(
    db_session: AsyncSession | None = None,
) -> AsyncGenerator[SatelliteService, None]:
    """Provide Satellites service.

    Args:
        db_session (AsyncSession | None, optional): current database session. Defaults to None.

    Returns:
        SatelliteService: An Satellite service object
    """
    async with SatelliteService.new(
        session=db_session,
    ) as service:
        yield service
