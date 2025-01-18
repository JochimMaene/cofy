from godot.core.tempo import Epoch
from litestar import post
from pydantic import NaiveDatetime

from app.domain.time.dtos import TimeConversionInput


@post("/time", summary="Time scale converter", tags=["Utilities"])
async def convert_time(data: TimeConversionInput) -> NaiveDatetime:
    e = Epoch(data.date.strftime("%Y-%m-%dT%H:%M:%S") + " " + data.from_time_scale)
    return e.calStr(data.to_time_scale).split()[0]
