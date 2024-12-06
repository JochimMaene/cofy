from __future__ import annotations

from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from app.db.models import Satellite

__all__ = ("SatelliteRepository",)


class SatelliteRepository(SQLAlchemyAsyncRepository[Satellite]):
    model_type = Satellite
