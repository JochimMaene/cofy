from __future__ import annotations

from typing import TYPE_CHECKING

from app.domain.ground_station.services import GroundStationService

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from sqlalchemy.ext.asyncio import AsyncSession

__all__ = ["provide_ground_station_service"]


async def provide_ground_station_service(
    db_session: AsyncSession | None = None,
) -> AsyncGenerator[GroundStationService, None]:
    """Provide GroundStations service.

    Args:
        db_session (AsyncSession | None, optional): current database session. Defaults to None.

    Returns:
        GroundStationService: An GroundStation service object
    """
    async with GroundStationService.new(
        session=db_session,
    ) as service:
        yield service
