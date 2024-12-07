from __future__ import annotations

from typing import TYPE_CHECKING

from advanced_alchemy.base import UUIDAuditBase
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from .satellite import Satellite


class Dynamics(UUIDAuditBase):
    __tablename__ = "dynamics"
    name: Mapped[str] = mapped_column(index=True)
    harmonics_degree: Mapped[int]
    harmonics_order: Mapped[int]
    solar_radiation_pressure: Mapped[bool]
    drag: Mapped[bool]
    solid_tides: Mapped[bool]
    third_body_sun: Mapped[bool]
    third_body_moon: Mapped[bool]
    satellites: Mapped[list[Satellite]] = relationship(
        back_populates="dynamics",
        lazy="noload",
        uselist=True,
        cascade="all, delete",
        viewonly=True,
    )
