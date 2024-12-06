from litestar.contrib.sqlalchemy.base import UUIDAuditBase


class OdpConfiguration(BaseModel):
    epoch: str = Field(description="Reference time, used as starting point for orbit propagation.")
    arc_start: str = Field(description="Start of the orbit propagation/determination arc.")
    arc_end: str = Field(description="End of the orbit propagation/determination arc.")


class OdpUniverseConfigGenSc(BaseModel):
    name: str
    file: str | None = Field(
        description="This includes an orbit file in the universe frames. If a trajectory configuration is provided,\
                               the orbit file is used to determine the default initial state. If a trajectory configuration is\
                               omitted, there will be no propagation and the orbit file will be simply interpolated.",
    )
    dynamics: str | None


class OdpUniverseConfigGen(BaseModel):
    uni_files: list[str] = Field(description="Configuration or subconfiguration of universe.", alias="uniFiles")
    sc_list: list[OdpUniverseConfigGenSc] = Field(
        description="Dynamics models to be used as templates and prepared for propagation in trajectory.\
                               This copies the models to objects with spacecraft specific names and creates corresponding\
                               parameters. The template names must be separated by a ',' (eg grav, srp, drag) and must match\
                               names of a dynamics model in the universe.",
    )


class OdpUniverse(BaseModel):
    cfgGen: OdpUniverseConfigGen = Field(
        description="Input for the configuration generator to generate a universe configuration file.",
    )


class OdpTrajectoryConfigGen(BaseModel):
    name: str = Field(description="Spacecraft name, must match the spacecraft name in the universe.")
    dynamics: str = Field(
        description="Dynamic model to be used in the trajectory propagation.\
                           Must match a model available in the universe.",
    )
    man_file: str = Field(description="Maneuver file in json format.", alias="manFile")


class OpdTrajectory(BaseModel):
    cfgGen: OdpTrajectoryConfigGen


class Parameter(BaseModel):
    name: str = Field(
        description="Parameter name, a partial name may be specified (eg cd instead of drag_cd).\
                            It is possible to provide several partial names separated by a '/' (eg pos_x/pos_y)\
                            The use of '/' allows to specify groups of parameters, while controlling their order.\
                            The provided expression may match zero, one or several parameters.",
    )
    weight: str | None = Field(
        description="Weight of the parameter, including units\
                            When specifying weight, all matched parameters must have the same unit.",
    )
    consider: bool = Field(False, description="Flag to set parameter as consider")
    covariance: list[list[str]] = Field(
        description="Covariance matrix. Allows to specify a possibly non-diagonal apriori\
                            covariance matrix. The matrix size must be the same as the number of\
                            matched parameter names. The parameters may have different units.",
    )


class Observation(BaseModel):
    name: str = Field(
        description="Name of the observation datasets.\
                            This can be anything and serves as a unique identifier for the dataset.",
    )
    type: str = Field(description="Type of observations. The type must be supported by odp.")
    weight: str = Field(description="Weight of the observations, including units")
    file: str = Field(description="Prepro database file with observation data in json format.")


class OdpProblemConfigGen(BaseModel):
    parameters: list[Parameter] = Field(
        description="List of parameters to be set as free (or consider).\
                    This entry is optional. It is typically omitted when computing\
                    observation residuals without parameter estimation.",
    )
    obervations: list[Observation] = Field(
        description="List of observation datasets.\
                    This entry is optional. When omitted, there will be no observations and free parameters\
                    will be constrained by their aproris only. It is typically omitted when propagating covariance.",
    )


class OdpProblem(BaseModel):
    cfgGen: OdpProblemConfigGen | None = Field(
        description="Input for the configuration generator to generate a problem configuration file.",
    )


class Odp(BaseModel):
    cfg: OdpConfiguration = Field(description="Generic odp configuration")
    universe: OdpUniverse = Field(description="Universe configuration and options. This entry is mandatory.")
    trajectory: list[OpdTrajectory] | None = Field(
        description="Trajectory configurations and options. This entry is optional.\
               It is typically omitted when working with fixed orbits.",
    )
    problem: OdpProblem | None = Field(
        description="Problem configuration and options. This entry is optional.\
               It is typically omitted when running a propagation only.",
    )
    plotFile: str | None = Field(description="Residuals plot in picture format specified by file suffix, eg jpg")
    jsonFile: str | None = Field(
        description="Residuals plot data in json format, ready to be used as input for the plotter",
    )


from __future__ import annotations

from datetime import datetime

from sqlalchemy.orm import Mapped, relationship

from app.db.models import Satellite
from app.lib.schema import CamelizedBaseStruct

__all__ = ["GroundStation"]


class State(CamelizedBaseStruct):
    pos_x: float
    pos_y: float
    pos_z: float
    vel_x: float
    vel_y: float
    vel_z: float


class ODSettings(CamelizedBaseStruct):
    arc_start: datetime
    arc_end: datetime
    rms_threshold: float
    max_iterations: int
    estimate_cd: bool
    estimate_cr: bool


class OrbitDetermination(UUIDAuditBase):
    __tablename__ = "orbit_determination"
    satellite: Mapped[Satellite] = relationship(
        back_populates="orbit_determinations",
        innerjoin=True,
        uselist=False,
        # lazy="noload",
    )

    start_estimation: Mapped[datetime]
    end_estimation: Mapped[datetime]
    initial_station: Mapped[State | str]
