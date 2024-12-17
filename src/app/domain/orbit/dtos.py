from advanced_alchemy.extensions.litestar.dto import SQLAlchemyDTO

from app.db.models import Orbit
from app.lib import dto

__all__ = ["OrbitCreateDTO", "OrbitDTO", "OrbitUpdateDTO"]


class OrbitDTO(SQLAlchemyDTO[Orbit]):
    config = dto.config(exclude={"created_at", "updated_at"})


class OrbitCreateDTO(SQLAlchemyDTO[Orbit]):
    config = dto.config(exclude={"id", "created_at", "updated_at", "satellite"})


class OrbitUpdateDTO(SQLAlchemyDTO[Orbit]):
    config = dto.config(exclude={"id", "created_at", "updated_at", "satellite"}, partial=True)
