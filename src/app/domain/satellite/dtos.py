from advanced_alchemy.extensions.litestar.dto import SQLAlchemyDTO

from app.db.models import Satellite
from app.lib import dto

__all__ = ["SatelliteCreateDTO", "SatelliteDTO", "SatelliteUpdateDTO"]


class SatelliteDTO(SQLAlchemyDTO[Satellite]):
    config = dto.config(exclude={"created_at", "updated_at"})


class SatelliteCreateDTO(SQLAlchemyDTO[Satellite]):
    config = dto.config(exclude={"id", "created_at", "updated_at"})


class SatelliteUpdateDTO(SQLAlchemyDTO[Satellite]):
    config = dto.config(exclude={"id", "created_at", "updated_at"}, partial=True)
