from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from app.db.models import TLE

from .repositories import TLERepository

__all__ = ("TLEService",)


class TLEService(SQLAlchemyAsyncRepositoryService[TLE]):
    repository_type = TLERepository
