from __future__ import annotations

from advanced_alchemy.repository import SQLAlchemyAsyncSlugRepository

from app.db.models import DataStatus

__all__ = ("DataStatusRepository",)


class DataStatusRepository(SQLAlchemyAsyncSlugRepository[DataStatus]):
    """DataStatus Repository."""

    model_type = DataStatus
