from typing import Optional
from pydantic import BaseModel, UUID4
from datetime import datetime


class GroundStationPass(BaseModel):
    satellite: UUID4
    ground_station: UUID4
    start: datetime
    end: datetime
    orbit_id: Optional[UUID4] = None


class NodeCrossing(BaseModel):
    satellite: UUID4
    ground_station: UUID4
    start: datetime
    end: datetime
    orbit_id: Optional[UUID4] = None
