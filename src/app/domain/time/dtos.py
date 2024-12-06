from typing import Literal

from pydantic import BaseModel, NaiveDatetime

TIME_SCALES = Literal["TT", "UTC", "GPS", "TAI", "TCG"]


class TimeConversionInput(BaseModel):
    date: NaiveDatetime
    from_time_scale: TIME_SCALES
    to_time_scale: TIME_SCALES
