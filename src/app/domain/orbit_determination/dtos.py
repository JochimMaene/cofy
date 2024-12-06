from typing import Literal, Optional

from pydantic import BaseModel, Field

EphemerisType = Literal["navsol.csv", "oem.txt", "oem.json", "oem.kvn"]

class Parameter(BaseModel):
    name: str = Field(description="Parameter name, a partial name may be specified (eg cd instead of drag_cd).\
                            It is possible to provide several partial names separated by a '/' (eg pos_x/pos_y)\
                            The use of '/' allows to specify groups of parameters, while controlling their order.\
                            The provided expression may match zero, one or several parameters.")
    weight: Optional[str] = Field(description="Weight of the parameter, including units\
                            When specifying weight, all matched parameters must have the same unit.")
    consider: bool = Field(False,description="Flag to set parameter as consider")
    covariance: list[list[str]] = Field(description="Covariance matrix. Allows to specify a possibly non-diagonal apriori\
                            covariance matrix. The matrix size must be the same as the number of\
                            matched parameter names. The parameters may have different units.")

class Observation(BaseModel):
    name: str = Field(description="Name of the observation datasets.\
                            This can be anything and serves as a unique identifier for the dataset.")
    type: str = Field(description="Type of observations. The type must be supported by odp.")
    weight: str = Field(description="Weight of the observations, including units")
    file: str = Field(description="Prepro database file with observation data in json format.")


class InitialState(BaseModel):
    x: float
    y: float
    z: float
    vx: float
    vy: float
    vz: float


class ODSettings(BaseModel):
    epoch: str
    arc_start: str
    arc_end: str
    rms_threshold: float
    max_iterations: int
    estimate_cd: bool
    estimate_cr: bool


class OD(BaseModel):
    initial_orbit: str | InitialState
    observations: list[Observation]
    satellite_id: str

    settings: ODSettings

    initial_trajectory: str

