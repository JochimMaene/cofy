from __future__ import annotations

from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from app.db.models import GroundStation

__all__ = ("GroundStationRepository",)


class GroundStationRepository(SQLAlchemyAsyncRepository[GroundStation]):
    """GroundStation Repository."""

    model_type = GroundStation
