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


def add_satellite_dynamics_to_config(uni_config: dict, dynamics: Dynamics, satellite: Satellite) -> None:
    uni_config["bodies"].append(
        {
            "name": "Earth",
            "point": "Earth",
            "gravity": ["EarthSphericalHarmonics"],
            "gm": "EarthSphericalHarmonics",
        },
        {"name": "Sun", "point": "Sun"},
        {"name": "Moon", "point": "Moon"},
    )


def get_dynamics_config(dynamics: Dynamics) -> dict:
    dynamics_config = {
        "bodies": [
            {
                "name": "Earth",
                "point": "Earth",
                "gravity": ["EarthSphericalHarmonics"],
                "gm": "EarthSphericalHarmonics",
            },
            {"name": "Sun", "point": "Sun"},
            {"name": "Moon", "point": "Moon"},
        ],
        "sphericalHarmonics": [
            {
                "name": "EarthSphericalHarmonics",
                "type": "File",
                "config": {
                    "point": "Earth",
                    "degree": dynamics.harmonics_degree,
                    "order": dynamics.harmonics_order,
                    "axes": "ITRF",
                    "file": "data/eigen05c_80_sha.tab",
                },
            },
        ],
        "gravity": [
            {
                "name": "EarthCenter",
                "bodies": [
                    "Earth",
                ],
            },
        ],
        "dynamics": [
            {"name": "gravity", "type": "SystemGravity", "config": {"model": "EarthCenter"}},
            # {
            #     "name": "srp",
            #     "type": "SimpleSRP",
            #     "config": {"occulters": ["Earth"], "mass": "satellite_mass", "area": "srp_area", "cr": "srp_cr"},
            # },
            {"name": "combined", "type": "Combined", "config": ["gravity"]},
        ],
    }
    if dynamics.third_body_sun:
        dynamics_config["gravity"][0]["bodies"].append("Sun")
    if dynamics.third_body_moon:
        dynamics_config["gravity"][0]["bodies"].append("Moon")

    if dynamics.solar_radiation_pressure:
        dynamics_config["dynamics"][-1]["config"].append("srp")

    return dynamics_config
