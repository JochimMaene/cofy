from advanced_alchemy.extensions.litestar.dto import SQLAlchemyDTO

from app.db.models.dynamics import Dynamics
from app.lib import dto

__all__ = ["DynamicsCreateDTO", "DynamicsDTO", "DynamicsUpdateDTO"]


class DynamicsDTO(SQLAlchemyDTO[Dynamics]):
    config = dto.config(exclude={"created_at", "updated_at", "satellites"})


class DynamicsCreateDTO(SQLAlchemyDTO[Dynamics]):
    config = dto.config(exclude={"id", "created_at", "updated_at", "satellites"})


class DynamicsUpdateDTO(SQLAlchemyDTO[Dynamics]):
    config = dto.config(exclude={"id", "created_at", "updated_at", "satellites"}, partial=True)
