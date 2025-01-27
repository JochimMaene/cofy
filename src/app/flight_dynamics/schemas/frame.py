from enum import Enum


class FrameType(str, Enum):
    ICRF = "ICRF"
    """"International Celestial Reference Frame"""

    TEME = "TEME"
    """True Equator Mean Equinox"""

    EME2000 = "EME2000"
    """Mean Equator Of Date at the epoch of J2000"""

    MOD = "MOD"
    """Mean Equator Of Date"""

    TOD = "TOD"
    """True Equator of Date"""

    ITRF = "ITRF"
    """ITRF frame (IERS2000)"""
