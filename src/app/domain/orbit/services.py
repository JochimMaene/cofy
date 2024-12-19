from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from app.db.models import IpfOrbit

from .repositories import OrbitRepository

__all__ = ("OrbitService",)


class OrbitService(SQLAlchemyAsyncRepositoryService[IpfOrbit]):
    repository_type = OrbitRepository
