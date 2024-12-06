from __future__ import annotations

from advanced_alchemy.repository import SQLAlchemyAsyncSlugRepository

from app.db.models.dynamics import Dynamics

__all__ = ["DynamicsRepository"]


class DynamicsRepository(SQLAlchemyAsyncSlugRepository[Dynamics]):
    model_type = Dynamics
