from datetime import datetime
from enum import Enum
from uuid import UUID

from advanced_alchemy.base import UUIDAuditBase
from advanced_alchemy.types import DateTimeUTC
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .satellite import Satellite


class TLEOrigin(str, Enum):
    spacetrack = "spacetrack"
    internal = "internal"


class TLE(UUIDAuditBase):
    __tablename__ = "tle"
    line1: Mapped[str]
    line2: Mapped[str]
    epoch: Mapped[datetime] = mapped_column(
        DateTimeUTC(timezone=True),
    )
    originator: Mapped[TLEOrigin]
    satellite_id: Mapped[UUID] = mapped_column(ForeignKey("satellite.id", ondelete="cascade"))
    satellite: Mapped[Satellite] = relationship(
        back_populates="tles",
        lazy="selectin",
        innerjoin=True,
        uselist=False,
    )
