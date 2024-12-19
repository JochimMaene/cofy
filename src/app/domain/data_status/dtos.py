from advanced_alchemy.extensions.litestar.dto import SQLAlchemyDTO

from app.db.models.data_status import DataStatus
from app.lib import dto

__all__ = ["DataStatusCreateDTO", "DataStatusDTO", "DataStatusUpdateDTO"]


class DataStatusDTO(SQLAlchemyDTO[DataStatus]):
    config = dto.config(exclude={"created_at", "updated_at"})


class DataStatusCreateDTO(SQLAlchemyDTO[DataStatus]):
    config = dto.config(exclude={"id", "created_at", "updated_at"})


class DataStatusUpdateDTO(SQLAlchemyDTO[DataStatus]):
    config = dto.config(exclude={"id", "created_at", "updated_at"}, partial=True)
