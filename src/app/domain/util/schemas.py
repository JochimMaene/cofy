from typing import Annotated, Optional
from datetime import datetime
from msgspec import Meta

from app.flight_dynamics.schemas.states import  StateType
from app.flight_dynamics.schemas.time import TimeScale, Epoch
from app.lib.schema import CamelizedBaseStruct


class StateConversionInput(CamelizedBaseStruct):
    from_state: StateType
    to_state: StateType
    state: Annotated[
        list[float],
        Meta(
            min_length=6,
            max_length=6,
            description="The 6 state elements for the input state. Units are km, km/s or radians depending on the input.",
        ),
    ]
    gm: Optional[float] = None


class StateConversionOutput(CamelizedBaseStruct):
    state: Annotated[list[float], Meta(min_length=6, max_length=6)]


class TimeScaleConversionInput(CamelizedBaseStruct):
    from_time_scale: TimeScale
    to_time_scale: TimeScale
    datetime: Annotated[datetime, Meta(tz=False)]


class TimeScaleConversionOutput(CamelizedBaseStruct):
    datetime: Annotated[datetime, Meta(tz=False)]

class FrameConversionInput(CamelizedBaseStruct):
    epoch: Epoch
    state: Annotated[list[float], Meta(min_length=6, max_length=6)]
    