from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from app.db.models import Satellite

from .repositories import SatelliteRepository

__all__ = ("SatelliteService",)


class SatelliteService(SQLAlchemyAsyncRepositoryService[Satellite]):
    repository_type = SatelliteRepository
