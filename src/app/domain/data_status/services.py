from __future__ import annotations

from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from advanced_alchemy.service import SQLAlchemyAsyncRepositoryService

from app.db import models as m

__all__ = ("DataStatusService",)

class DataStatusService(SQLAlchemyAsyncRepositoryService[m.DataStatus]):
    """Handles basic lookup operations for an Data Status."""

    class Repository(SQLAlchemyAsyncRepository[m.DataStatus]):
        """Data Status Repository."""

        model_type = m.DataStatus

    repository_type = Repository
    match_fields = ["name"]
