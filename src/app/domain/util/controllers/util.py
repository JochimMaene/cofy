from godot import cosmos
from godot.core.astro import convert
from godot.core.tempo import Epoch
from litestar import post
from litestar.controller import Controller
from litestar.dto import MsgspecDTO
from structlog import get_logger

from app.domain.accounts.guards import requires_active_user
from app.domain.util import urls
from app.domain.util.schemas import (
    StateConversionInput,
    StateConversionOutput,
    TimeScaleConversionInput,
    TimeScaleConversionOutput,
)
from app.lib.universe_assembler import uni_config

logger = get_logger()


class ConversionController(Controller):
    guards = [requires_active_user]
    tags = ["Utilities"]

    @post(
        operation_id="ConvertState",
        name="state:convert",
        summary="Convert State",
        description="Convert between state types.",
        guards=[requires_active_user],
        path=urls.CREATE_STATE_CONVERSION,
        dto=MsgspecDTO[StateConversionInput],
        return_dto=MsgspecDTO[StateConversionInput],
    )
    async def create_state_conversion(
        self,
        data: StateConversionInput,
    ) -> StateConversionOutput:
        uni = cosmos.Universe(uni_config)

        return StateConversionOutput(
            state=convert(
                data.from_state,
                data.to_state,
                data.state,
                {"gm": uni.constants.getMu("Earth")},
            ).tolist()
        )
    @post(
        operation_id="ConvertTimeScale",
        name="time_scale:convert",
        summary="Convert Time Scale",
        description="Convert between time scales.",
        guards=[requires_active_user],
        path=urls.CREATE_TIME_SCALE_CONVERSION,
        dto=MsgspecDTO[TimeScaleConversionInput],
        return_dto=MsgspecDTO[TimeScaleConversionOutput],
    )
    async def create_time_scale_conversion(
        self,
        data: TimeScaleConversionInput,
    ) -> TimeScaleConversionOutput:
        e = Epoch(f"{data.datetime.isoformat()} {data.from_time_scale.value}")
        return TimeScaleConversionOutput(datetime=e.calStr(data.to_time_scale).split()[0])