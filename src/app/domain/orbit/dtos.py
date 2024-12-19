from advanced_alchemy.extensions.litestar.dto import SQLAlchemyDTO

from app.db.models import IpfOrbit
from app.lib import dto

__all__ = ["OrbitCreateDTO", "OrbitDTO", "OrbitUpdateDTO"]


class OrbitDTO(SQLAlchemyDTO[IpfOrbit]):
    config = dto.config(exclude={"created_at", "updated_at"})


class OrbitCreateDTO(SQLAlchemyDTO[IpfOrbit]):
    config = dto.config(exclude={"id", "created_at", "updated_at", "satellite"})


class OrbitUpdateDTO(SQLAlchemyDTO[IpfOrbit]):
    config = dto.config(exclude={"id", "created_at", "updated_at", "satellite"}, partial=True)
