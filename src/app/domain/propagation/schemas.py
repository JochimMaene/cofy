from typing import Annotated
from uuid import UUID

from msgspec import Meta

from app.flight_dynamics.schemas.states import StateCart, StateCirc, StateKep
from app.lib.schema import CamelizedBaseStruct

UnionType = StateCart | StateKep | StateCirc


class JobRequest(CamelizedBaseStruct):
    location: Annotated[str, Meta(description="Location to check the status of the request.")]
    queue_id: Annotated[UUID, Meta(description="Queue id for the request.")]


class PropagationInput(CamelizedBaseStruct):
    satellite_id: UUID
    initial_orbit: UnionType
    initial_mass: float
    epoch_start: str
    epoch_end: str


class PropagationResult(CamelizedBaseStruct):
    orbit_id: UUID
    satellite_id: UUID
    execution_duration: float


def return_propagation_template(propagation_input: PropagationInput) -> dict:
    sc_name = propagation_input.satellite_id.hex
    return {
        "setup": [
            {
                "name": sc_name,
                "type": "group",
                "input": [
                    {"name": "center", "type": "point"},
                    {"name": "mass", "type": "scalar", "unit": "kg"},
                    {"name": "dv", "type": "scalar", "unit": "m/s"},
                ],
            },
        ],
        "timeline": [
            {
                "type": "control",
                "name": "initial",
                "epoch": propagation_input.epoch_start,
                "state": [
                    {
                        "name": sc_name + "_center",
                        "body": "Earth",
                        "axes": "ICRF",
                        "dynamics": "combined",
                        "value": propagation_input.initial_orbit.to_dict(),
                    },
                    {"name": sc_name + "_mass", "value": str(propagation_input.initial_mass) + " kg"},
                    {"name": sc_name + "_dv", "value": "0 m/s"},
                ],
            },
            {"type": "point", "name": "final", "input": sc_name, "point": {"epoch": propagation_input.epoch_end}},
        ],
    }
