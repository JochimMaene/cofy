from datetime import datetime

from pydantic import UUID4, BaseModel


class GroundStationPass(BaseModel):
    satellite: UUID4
    ground_station: UUID4
    start: datetime
    end: datetime
    orbit_id: UUID4 | None = None


class NodeCrossing(BaseModel):
    satellite: UUID4
    ground_station: UUID4
    start: datetime
    end: datetime
    orbit_id: UUID4 | None = None
