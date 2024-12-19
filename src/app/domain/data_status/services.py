from __future__ import annotations

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from app.db.models import DataStatus

from .repositories import DataStatusRepository

__all__ = ("DataStatusRepository",)


class DataStatusService(SQLAlchemyAsyncRepositoryService[DataStatus]):
    repository_type = DataStatusRepository
