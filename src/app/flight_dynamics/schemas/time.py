from datetime import datetime
from enum import Enum
from typing import Annotated

from msgspec import Meta

from app.lib.schema import CamelizedBaseStruct





class TimeScale(str, Enum):
    UTC = "UTC"
    """"Coordinated Universal Time"""

    TT = "TT"
    """Terrestrial Time"""

    TAI = "TAI"
    """International Atomic Time"""

    GPS = "GPS"
    """GPS Time"""


class Epoch(CamelizedBaseStruct):
    datetime: Annotated[datetime, Meta(tz=False)]
    time_scale: TimeScale
