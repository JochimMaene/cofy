from datetime import datetime
from enum import Enum
from uuid import UUID

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .satellite import Satellite


class OrbitType(Enum):
    IPF = 1
    TLE = 2
    OEM = 3


class Orbit(UUIDAuditBase):
    __tablename__ = "orbit"
    file_name: Mapped[str]
    type: Mapped[OrbitType]
    start: Mapped[datetime]
    end: Mapped[datetime]
    satellite_id: Mapped[UUID] = mapped_column(ForeignKey("satellite.id", ondelete="cascade"))
    satellite: Mapped[Satellite] = relationship(
        back_populates="orbits",
        innerjoin=True,
        uselist=False,
    )

    # satellite_id: Column(ForeignKey("satellite.id"))
    # trajectory_config: Mapped[Trajectory] = mapped_column(JsonB)
