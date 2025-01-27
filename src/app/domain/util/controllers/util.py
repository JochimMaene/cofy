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
    FrameConversionInput,
    FrameConversionOutput,
    StateConversionInput,
    StateConversionOutput,
    TimeScaleConversionInput,
    TimeScaleConversionOutput,
)
from app.flight_dynamics.schemas.assembler.universe import uni_config

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

    @post(
        operation_id="ConvertFrame",
        name="frame:convert",
        summary="Convert Frame",
        description="Convert between reference frames.",
        guards=[requires_active_user],
        path=urls.CREATE_FRAMES_CONVERSION,
        dto=MsgspecDTO[FrameConversionInput],
        return_dto=MsgspecDTO[FrameConversionOutput],
    )
    async def create_frame_conversion(
        self,
        data: FrameConversionInput,
    ) -> FrameConversionOutput:
        uni = cosmos.Universe(uni_config)


        print(data.state)
        print(data.from_frame.value)
        print(Epoch(f"{data.epoch.datetime.isoformat()} {data.epoch.time_scale.value}"))

        return FrameConversionOutput(
            state=uni.frames.rotate(
                data.state,
                data.from_frame.value,
                data.to_frame.value,
                Epoch(f"{data.epoch.datetime.isoformat()} {data.epoch.time_scale.value}"),
            ),
        )
