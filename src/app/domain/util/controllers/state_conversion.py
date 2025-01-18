from godot import cosmos
from litestar import post
from litestar.controller import Controller
from structlog import get_logger

from app.domain.accounts.guards import requires_active_user
from app.domain.util import urls
from app.domain.util.schemas import StateConversionInput, StateConversionOutput
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
        # dto=MsgspecDTO[StateConversionInput],
        # return_dto=MsgspecDTO[StateConversionInput],
    )
    async def create_state_conversion(
        self,
        data: StateConversionInput,
    ) -> StateConversionOutput:
        uni = cosmos.Universe(uni_config)
        # convert(data.state.)

        print(data.to_dict())

        return None
