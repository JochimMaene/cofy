from datetime import datetime
from uuid import UUID

from advanced_alchemy.base import UUIDAuditBase
from advanced_alchemy.types import DateTimeUTC
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .satellite import Satellite


class IpfOrbit(UUIDAuditBase):
    __tablename__ = "ipf_orbit"
    file_name: Mapped[str]
    start: Mapped[datetime] = mapped_column(
        DateTimeUTC(timezone=True),
    )
    end: Mapped[datetime] = mapped_column(
        DateTimeUTC(timezone=True),
    )
    satellite_id: Mapped[UUID] = mapped_column(ForeignKey("satellite.id", ondelete="cascade"))
    satellite: Mapped[Satellite] = relationship(
        back_populates="orbits",
        lazy="selectin",
        innerjoin=True,
        uselist=False,
    )


# class OemOrbit(UUIDAuditBase):
#     __tablename__ = "oem_orbit"
#     file_name: Mapped[str]
#     start: Mapped[datetime]
#     end: Mapped[datetime]
#     satellite_id: Mapped[UUID] = mapped_column(ForeignKey("satellite.id", ondelete="cascade"))
#     satellite: Mapped[Satellite] = relationship(
#         back_populates="orbits",
#         innerjoin=True,
#         uselist=False,
#     )
