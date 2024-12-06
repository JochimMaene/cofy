from advanced_alchemy.extensions.litestar.dto import SQLAlchemyDTO

from app.db.models.ground_station import GroundStation
from app.lib import dto

__all__ = ["GroundStationCreateDTO", "GroundStationDTO", "GroundStationUpdateDTO"]


class GroundStationDTO(SQLAlchemyDTO[GroundStation]):
    config = dto.config(exclude={"created_at", "updated_at"})


class GroundStationCreateDTO(SQLAlchemyDTO[GroundStation]):
    config = dto.config(exclude={"id", "created_at", "updated_at"})


class GroundStationUpdateDTO(SQLAlchemyDTO[GroundStation]):
    config = dto.config(exclude={"id", "created_at", "updated_at"}, partial=True)
