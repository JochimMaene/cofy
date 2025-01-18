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
    dynamics_config: dict = {
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
            {"name": "combined", "type": "Combined", "config": ["gravity"]},
        ],
    }

    if dynamics.drag:
        dynamics_config["atmosphere"] = [
            {
                "name": "EarthAtmos",
                "type": "nrlmsise00",
                "config": {"point": "Earth", "axes": "ITRF", "file": "data/space_weather.ipf"},
            },
        ]
        dynamics_config["dynamics"][-1]["config"].append("drag")
        dynamics_config["dynamics"].insert(
            0,
            {
                "name": "drag",
                "type": "SimpleDrag",
                "config": {
                    "atmosphere": "EarthAtmos",
                    "mass": satellite.dry_mass,  # TODO: add the wet mass
                    "area": str(satellite.drag_area) + " m^2",
                    "cd": satellite.drag_coefficient,
                },
            },
        )
    if dynamics.third_body_sun:
        dynamics_config["gravity"][0]["bodies"].append("Sun")
    if dynamics.third_body_moon:
        dynamics_config["gravity"][0]["bodies"].append("Moon")

    if dynamics.solar_radiation_pressure:
        dynamics_config["dynamics"][-1]["config"].append("srp")
        dynamics_config["dynamics"].insert(
            0,
            {
                "name": "srp",
                "type": "SimpleSRP",
                "config": {
                    "occulters": ["Earth"],
                    "mass": satellite.dry_mass,  # TODO: add the wet mass
                    "area": str(satellite.srp_area) + " m^2",
                    "cr": satellite.srp_coefficient,
                },
            },
        )

    if dynamics.solid_tides:
        dynamics_config["sphericalHarmonics"].append(
            {
                "name": "EarthSolidTides",
                "type": "EarthTides",
                "config": {"base": "EarthSphericalHarmonics", "solidTides": "data/solid_tides.tab"},
            },
        )

    return dynamics_config
