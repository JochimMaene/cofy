from __future__ import annotations

from typing import TYPE_CHECKING, Annotated, Literal
from uuid import UUID

from advanced_alchemy.base import UUIDAuditBase
from msgspec import Meta
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.lib.schema import CamelizedBaseStruct

if TYPE_CHECKING:
    from .dynamics import Dynamics
    from .orbit import Orbit


class TleConfig(CamelizedBaseStruct):
    norad_id: Annotated[int, Meta(description="The norad id as on spacetrack.")]
    classification: Literal["U", "C"]
    launch_year: int
    launch_number: int
    piece_of_launch: str


class PropulsionSystem(CamelizedBaseStruct):
    name: str
    direction: str
    isp: float
    thrust_level: float
    min_burn_duration: float
    max_burn_duration: float


class GnssSensor(CamelizedBaseStruct):
    name: str
    pos_x_std: float
    pos_y_std: float
    pos_z_std: float
    vel_std: float


class Aocs(CamelizedBaseStruct):
    name: str
    maximum_ang_vel: float


class Satellite(UUIDAuditBase):
    # __tablename__ = "satellites"
    name: Mapped[str] = mapped_column(index=True)
    group: Mapped[str] = mapped_column(index=True, nullable=True)
    dry_mass: Mapped[float]
    drag_area: Mapped[float]
    drag_coefficient: Mapped[float]
    srp_area: Mapped[float]
    srp_coefficient: Mapped[float] = mapped_column(
        doc="test",
    )
    # tle_config_id: Mapped[UUID] = Column(ForeignKey("tle_config.id"),info=dto_field("private"))
    # tle_config: Mapped[TleConfig] = relationship("TleConfig")
    tle_config: Mapped[TleConfig] = mapped_column(
        JSONB,
        doc="test",
    )
    propulsion: Mapped[PropulsionSystem] = mapped_column(JSONB)
    aocs: Mapped[Aocs] = mapped_column(JSONB)
    gnss: Mapped[GnssSensor] = mapped_column(JSONB)
    # dynamics_config: Mapped[str]
    # main_orbit_id: Mapped[UUID] = mapped_column(nullable=True)

    dynamics_id: Mapped[UUID] = mapped_column(ForeignKey("dynamics.id", ondelete="cascade"))
    # main_orbit_id: Mapped[UUID] = mapped_column(ForeignKey("orbit.id", ondelete="cascade"))
    # # -----------
    # # ORM Relationships
    # # ------------

    # relationship()
    orbits: Mapped[list[Orbit]] = relationship(
        back_populates="satellite",
        lazy="noload",
        uselist=True,
        viewonly=True,
    )

    # main_orbit: Mapped[Orbit] = relationship(
    #     back_populates="satellite",
    #     innerjoin=True,
    #     uselist=False,
    #     # lazy="noload",
    # )

    dynamics: Mapped[Dynamics] = relationship(
        back_populates="satellites",
        innerjoin=True,
        uselist=False,
        # lazy="noload",
    )
