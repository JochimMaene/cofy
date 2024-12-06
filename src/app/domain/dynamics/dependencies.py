from __future__ import annotations

from typing import TYPE_CHECKING

from app.domain.dynamics.services import DynamicsService

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from sqlalchemy.ext.asyncio import AsyncSession

__all__ = ["provide_dynamics_service"]


async def provide_dynamics_service(
    db_session: AsyncSession | None = None,
) -> AsyncGenerator[DynamicsService, None]:
    """Provide Dynamicss service.

    Args:
        db_session (AsyncSession | None, optional): current database session. Defaults to None.

    Returns:
        DynamicsService: An Dynamics service object
    """
    async with DynamicsService.new(
        session=db_session,
    ) as service:
        yield service
