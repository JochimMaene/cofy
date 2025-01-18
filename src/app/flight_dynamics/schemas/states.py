from enum import Enum
from typing import Annotated

from msgspec import Meta

from app.lib.schema import CamelizedBaseStruct

__all__ = ("AnyState", "StateCart", "StateCirc", "StateKep", "StateType")


class StateCart(CamelizedBaseStruct, tag_field=None, tag=True):
    pos_x: Annotated[str, Meta(description="Position vector X component.", examples=["7000 km"])]
    pos_y: Annotated[str, Meta(description="Position vector Y component.", examples=["150.5 km"])]
    pos_z: Annotated[str, Meta(description="Position vector Z component.", examples=["150.5 km"])]
    vel_x: Annotated[str, Meta(description="Velocity vector X component.", examples=["3.6 km/s", "514 m/s"])]
    vel_y: Annotated[str, Meta(description="Velocity vector Y component.", examples=["3.6 km/s", "514 m/s"])]
    vel_z: Annotated[str, Meta(description="Velocity vector Z component.", examples=["3.6 km/s", "514 m/s"])]


class StateKep(CamelizedBaseStruct, tag_field=None, tag=True):
    sma: Annotated[str, Meta(description="Semi-major axis", examples=["42165 km"])]
    ecc: Annotated[float, Meta(description="Eccentricity", examples=["0.01"])]
    inc: Annotated[str, Meta(description="Inclination", examples=["70 deg"])]
    ran: Annotated[str, Meta(description="Right-ascension of the ascending node", examples=["32.9 deg"])]
    aop: Annotated[str, Meta(description="Argument of pericentre", examples=["32.9 deg"])]
    tan: Annotated[str, Meta(description="True anomaly", examples=["-37.3 deg"])]


class StateCirc(CamelizedBaseStruct, tag_field=None, tag=True):
    sma: Annotated[str, Meta(description="Semi-major axis.", examples=["7500 km"])]
    ecx: float
    ecy: float
    inc: str
    ran: str
    aol: str


class StateType(str, Enum):
    cartesian = "Cart"
    keplerian = "Kep"
    circular = "Circ"


AnyState = StateCart | StateKep | StateCirc


class TimeScale(str, Enum):
    UTC = "UTC"
    """"Coordinated Universal Time"""

    TT = "TT"
    """Terrestrial Time"""

    TAI = "TAI"
    """International Atomic Time"""

    GPS = "GPS"
    """GPS Time"""
