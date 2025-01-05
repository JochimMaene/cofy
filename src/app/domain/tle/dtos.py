from advanced_alchemy.extensions.litestar.dto import SQLAlchemyDTO

from app.db.models import TLE
from app.lib import dto

__all__ = ["TLEDTO"]


class TLEDTO(SQLAlchemyDTO[TLE]):
    config = dto.config(exclude={"created_at", "updated_at", "satellite"})
