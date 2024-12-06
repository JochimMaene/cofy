from __future__ import annotations

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from app.db.models import Dynamics

from .repositories import DynamicsRepository

__all__ = ("DynamicsRepository",)


class DynamicsService(SQLAlchemyAsyncRepositoryService[Dynamics]):
    repository_type = DynamicsRepository
