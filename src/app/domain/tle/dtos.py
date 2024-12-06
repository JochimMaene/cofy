from datetime import datetime
from typing import Optional

from app.domain.satellite.models import Satellite
from pydantic import UUID4, BaseModel, Field


class TLE_Gen(BaseModel):
    satellite: UUID4
    orbit: UUID4
    begin: datetime = Field(description="Begin epoch")
    end: datetime = Field(description="End epoch")
    step: Optional[str] = Field("1d", description="Generate TLEs with this step")
    manoeuvre_file: Optional[str]
    bstar_fit: Optional[bool] = Field(False,description="Flag to use B-star fitting.")
    output_file_path: str = Field(description="Output file path for the TLEs")

def generate_input(tle_gen: TLE_Gen, satellite: Satellite):
    tle_config = satellite.tle_config

    {
        "description": None,
        "universe": [None],
        "spacecraft": {"name": satellite.name, "orbitFile": "string"},
        "begin": tle_gen.begin,
        "end": tle_gen.end,
        "step": tle_gen.step,
        "minimumStep": None,
        "manoeuvreFile": tle_gen.manoeuvre_file,
        "tleFit":{"bStarFit":tle_gen.bstar_fit},
        "spaceCraftData": {
            "satelliteNumber": tle_config.norad_id,
            "classification": tle_config.classification,
            "yearOfLaunch": tle_config.launch_year,
            "launchNumber": tle_config.launch_number,
            "pieceOfLaunch": tle_config.piece_of_launch,
            "orbitNumbersFile":None,
        },
        "outputFile": tle_gen.output_file_path
    }
