from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from app.db.models import Orbit

from .repositories import OrbitRepository

__all__ = ("OrbitService",)


class OrbitService(SQLAlchemyAsyncRepositoryService[Orbit]):
    repository_type = OrbitRepository
