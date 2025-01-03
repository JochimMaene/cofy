from __future__ import annotations

from advanced_alchemy.repository import SQLAlchemyAsyncRepository

from app.db.models import TLE

__all__ = ("TLERepository",)


class TLERepository(SQLAlchemyAsyncRepository[TLE]):
    model_type = TLE
