from app.db.models import Dynamics, Satellite


def add_satellite_dynamics_to_config(uni_config: dict, dynamics: Dynamics, satellite: Satellite) -> None:
    uni_config["bodies"].append(
        {
            "name": "Earth",
            "point": "Earth",
            "gravity": ["EarthSphericalHarmonics"],
            "gm": "EarthSphericalHarmonics",
        },
        {"name": "Sun", "point": "Sun"},
        {"name": "Moon", "point": "Moon"},
    )


def get_dynamics_config(dynamics: Dynamics, satellite: Satellite) -> dict:
    dynamics_config = {
        "bodies": [
            {
                "name": "Earth",
                "point": "Earth",
                "gravity": ["EarthSphericalHarmonics"],
                "gm": "EarthSphericalHarmonics",
            },
            {"name": "Sun", "point": "Sun"},
            {"name": "Moon", "point": "Moon"},
        ],
        "sphericalHarmonics": [
            {
                "name": "EarthSphericalHarmonics",
                "type": "File",
                "config": {
                    "point": "Earth",
                    "degree": dynamics.harmonics_degree,
                    "order": dynamics.harmonics_order,
                    "axes": "ITRF",
                    "file": "data/eigen05c_80_sha.tab",
                },
            },
        ],
        "gravity": [
            {
                "name": "EarthCenter",
                "bodies": [
                    "Earth",
                ],
            },
        ],
        "dynamics": [
            {"name": "gravity", "type": "SystemGravity", "config": {"model": "EarthCenter"}},
            {
                "name": "srp",
                "type": "SimpleSRP",
                "config": {
                    "occulters": ["Earth"],
                    "mass": 100,
                    "area": satellite.srp_area,
                    "cr": satellite.srp_coefficient,
                },
            },
            {"name": "combined", "type": "Combined", "config": ["gravity"]},
        ],
    }
    if dynamics.third_body_sun:
        dynamics_config["gravity"][0]["bodies"].append("Sun")
    if dynamics.third_body_moon:
        dynamics_config["gravity"][0]["bodies"].append("Moon")

    if dynamics.solar_radiation_pressure:
        dynamics_config["dynamics"][-1]["config"].append("srp")

    return dynamics_config
