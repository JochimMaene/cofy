from __future__ import annotations

from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from app.db import models as m

__all__ = ("TLEService",)


class TLEService(SQLAlchemyAsyncRepositoryService[m.TLE]):
    """Handles basic lookup operations for an TLE."""

    class Repository(SQLAlchemyAsyncRepository[m.TLE]):
        """TLE Repository."""

        model_type = m.TLE

    repository_type = Repository
    match_fields = ["name"]