from datetime import datetime
from typing import Annotated
from uuid import UUID

from msgspec import Meta

from app.lib.schema import CamelizedBaseStruct


class TLEOrbitCreate(CamelizedBaseStruct):
    TLE: Annotated[
        list[str],
        Meta(
            description="TLE as a list of two elements, representing the two lines.",
            examples=["150.5 km"],
            min_length=2,
            max_length=2,
        ),
    ]
    start: Annotated[datetime, Meta(description="Start of validity of TLE")]
    end: Annotated[datetime, Meta(description="End of validity of TLE")]
    satellite: Annotated[UUID, Meta(description="Satellite id", examples=["fae33a8d-f73a-4772-b1f1-b422fce525cb"])]
