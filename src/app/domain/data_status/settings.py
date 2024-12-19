from collections.abc import Callable
from dataclasses import dataclass

from app.lib import data

__all__ = ["ENVIRONMENT_DATA_SETTINGS"]


@dataclass
class EnvironementDataUpdateSettings:
    name: str
    URL: str
    cron: str | None
    file_name: str
    update_func: Callable


URL_LEAP_SECONDS = "https://astroutils.astronomy.osu.edu/time/tai-utc.txt"
URL_SPACE_WEATHER = "https://celestrak.org/SpaceData/SW-Last5Years.csv"
URL_EOP = "https://datacenter.iers.org/data/csv/finals2000A.data.csv"
URL_JPL = "https://ssd.jpl.nasa.gov/ftp/eph/planets/bsp/de440s.bsp"

ENVIRONMENT_DATA_SETTINGS = {
    1: EnvironementDataUpdateSettings(
        name="Leap seconds",
        URL=URL_LEAP_SECONDS,
        cron="0 2 * * *",
        file_name="leap_seconds.txt",
        update_func=data.update_leap_second_data,
    ),
    2: EnvironementDataUpdateSettings(
        name="Space weather",
        URL=URL_SPACE_WEATHER,
        cron="0 2 * * *",
        file_name="space_weather.ipf",
        update_func=data.back_ground_space_weather,
    ),
    3: EnvironementDataUpdateSettings(
        name="Earth orientation parameters",
        URL=URL_EOP,
        cron="0 2 * * *",
        file_name="erp.ipf",
        update_func=data.back_ground_eop,
    ),
    4: EnvironementDataUpdateSettings(
        name="JPL ephermeris",
        URL=URL_JPL,
        cron=None,
        file_name="de440",
        update_func=data.download_JPL_ephemeris,
    ),
}
