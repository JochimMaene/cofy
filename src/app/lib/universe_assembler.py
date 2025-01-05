# file version number

uni_config: dict = {
    "version": "3.0",
    "spacetime": {"system": "GCRS"},
    "ephemeris": [
        {
            "name": "de440",
            "files": ["data/de440"],
        },
    ],
    "constants": {
        "ephemeris": [
            {
                "source": "de440",
            },
        ],
    },
    "frames": [
        {"name": "ephem", "type": "Ephem", "config": {"source": "de440"}},
        {
            "name": "ITRF",
            "type": "AxesOrient",
            "config": {"model": "IERS2000", "nutation": "data/nutation2000A.ipf", "erp": "data/erp.ipf"},
        },
        {"name": "TEME", "type": "AxesOrient", "config": {"model": "TEME", "nutation": "data/nutation2000A.ipf"}},
    ],
    "bodies": [
        {
            "name": "Sun",
            "point": "Sun",
        },
        {
            "name": "Earth",
            "point": "Earth",
        },
        {
            "name": "Moon",
            "point": "Moon",
        },
    ],
}
