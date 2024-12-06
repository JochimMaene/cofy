from __future__ import annotations

from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from app.db.models import Orbit

__all__ = ("OrbitRepository",)


class OrbitRepository(SQLAlchemyAsyncRepository[Orbit]):
    model_type = Orbit
