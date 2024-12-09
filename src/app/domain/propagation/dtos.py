from typing import Annotated
from uuid import UUID

from msgspec import Meta

from app.lib.schema import CamelizedBaseStruct


class StateCart(CamelizedBaseStruct, tag=True):
    pos_x: Annotated[str, Meta(description="Position vector X component.", examples=["150.5 km"])]
    pos_y: Annotated[str, Meta(description="Position vector Y component.", examples=["150.5 km"])]
    pos_z: Annotated[str, Meta(description="Position vector Z component.", examples=["150.5 km"])]
    vel_x: Annotated[str, Meta(description="Velocity vector X component.", examples=["3.6 km/s", "514 m/s"])]
    vel_y: Annotated[str, Meta(description="Velocity vector Y component.", examples=["3.6 km/s", "514 m/s"])]
    vel_z: Annotated[str, Meta(description="Velocity vector Z component.", examples=["3.6 km/s", "514 m/s"])]


class StateKep(CamelizedBaseStruct, tag=True):
    sma: Annotated[str, Meta(description="Semi-major axis", examples=["42165 km"])]
    ecc: Annotated[float, Meta(description="Eccentricity", examples=["0.01"])]
    inc: Annotated[str, Meta(description="Inclination", examples=["70 deg"])]
    ran: Annotated[str, Meta(description="Right-ascension of the ascending node", examples=["32.9 deg"])]
    aop: Annotated[str, Meta(description="Argument of pericentre", examples=["32.9 deg"])]
    tan: Annotated[str, Meta(description="True anomaly", examples=["-37.3 deg"])]


class StateCirc(CamelizedBaseStruct, tag=True):
    sma: Annotated[str, Meta(description="Semi-major axis.", examples=["7500 km"])]
    ecx: float
    ecy: float
    inc: str
    ran: str
    aol: str


class JobRequest(CamelizedBaseStruct):
    location: Annotated[str, Meta(description="Location to check the status of the request.")]
    queue_id: Annotated[UUID, Meta(description="Queue id for the request.")]


class PropagationInput(CamelizedBaseStruct):
    satellite: UUID
    initial_orbit: StateKep
    initial_mass: float
    epoch_start: str
    epoch_end: str


class PropagationResult(CamelizedBaseStruct):
    orbit_id: UUID
    satellite_id: UUID
    execution_duration: float


def return_propagation_template(propagation_input: PropagationInput) -> dict:
    sc_name = propagation_input.satellite.hex
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
