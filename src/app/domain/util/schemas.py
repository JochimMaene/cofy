from datetime import datetime
from typing import Annotated

from msgspec import Meta

from app.flight_dynamics.schemas.states import AnyState, StateType, TimeScale
from app.lib.schema import CamelizedBaseStruct


class StateConversionInput(CamelizedBaseStruct):
    state: AnyState
    to_state: StateType
    epoch: Annotated[datetime, Meta(tz=False)]
    time_scale: TimeScale


class StateConversionOutput(CamelizedBaseStruct):
    state: StateType
