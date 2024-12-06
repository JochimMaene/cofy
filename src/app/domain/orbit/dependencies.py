from __future__ import annotations

from typing import TYPE_CHECKING

from app.domain.orbit.services import OrbitService

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from sqlalchemy.ext.asyncio import AsyncSession

__all__ = ["provide_orbit_service"]


async def provide_orbit_service(
    db_session: AsyncSession | None = None,
) -> AsyncGenerator[OrbitService, None]:
    """Provide Orbits service.

    Args:
        db_session (AsyncSession | None, optional): current database session. Defaults to None.

    Returns:
        OrbitService: An Orbit service object
    """
    async with OrbitService.new(
        session=db_session,
    ) as service:
        yield service
