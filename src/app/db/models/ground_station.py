from __future__ import annotations

from litestar.contrib.sqlalchemy.base import UUIDAuditBase
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.lib.schema import CamelizedBaseStruct

__all__ = ["GroundStation"]


class ElevationMaskPoint(CamelizedBaseStruct):
    azimuth: float
    elevation: float


class GroundStation(UUIDAuditBase):
    __tablename__ = "ground_station"
    name: Mapped[str]
    group: Mapped[str] = mapped_column(nullable=True)
    longitude: Mapped[float]
    latitude: Mapped[float]
    altitude: Mapped[float]
    elevation_mask: Mapped[list[ElevationMaskPoint]] = mapped_column(JSONB)
