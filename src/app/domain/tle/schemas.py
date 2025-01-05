from uuid import UUID

from app.lib.schema import CamelizedBaseStruct


class TleGenerationFromOrbitInput(CamelizedBaseStruct):
    # satellite_id: UUID
    orbit_id: UUID
    step: float
    # begin_fit: datetime
    # end_fit: datetime
