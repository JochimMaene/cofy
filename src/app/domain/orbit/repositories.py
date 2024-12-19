from __future__ import annotations

from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from app.db.models import IpfOrbit

__all__ = ("OrbitRepository",)


class OrbitRepository(SQLAlchemyAsyncRepository[IpfOrbit]):
    model_type = IpfOrbit
