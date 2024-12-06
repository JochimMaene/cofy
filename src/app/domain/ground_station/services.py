from __future__ import annotations

from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from app.db.models import GroundStation

from .repositories import GroundStationRepository

__all__ = ("GroundStationService",)


class GroundStationService(SQLAlchemyAsyncRepositoryService[GroundStation]):
    repository_type = GroundStationRepository
