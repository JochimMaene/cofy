import math
from uuid import uuid4

import numpy as np
from godot import cosmos, model
from godot.core import astro, num, tempo
from numpy.typing import ArrayLike, NDArray
from structlog import get_logger

from app.db.models import IpfOrbit
from app.lib.exceptions import MaxIterationsExceededError
from app.lib.universe_assembler import uni_config

logger = get_logger()


class StateEqui(model.geometry.StateConverter):
    def __init__(self, uni: cosmos.Universe, satellite: str) -> None:
        super().__init__(
            "Cart",
            "Equi",
            model.geometry.Vector6(uni.frames, "Earth", satellite, "ICRF"),
            {"gm": uni.bodies.get("Earth").gmProvider()},
        )


class TwoLineElement:
    """Two Line Element representation and handling"""

    def __init__(
        self,
        uni: cosmos.Universe,
        epoch: tempo.Epoch,
        pars: ArrayLike,
        tle_config: dict | None = None,
        element_number: int = 999,
        revolution_number: int = 0,
    ) -> None:
        if tle_config is None:
            self.norad_id = 99999
            self.classification = "U"
            self.launch_number = 999
            self.piece_of_launch = "XXX"
            self.year_of_launch = 2000
        else:
            self.norad_id = tle_config["noradId"]
            self.classification = tle_config["classification"]
            self.launch_number = tle_config["launchNumber"]
            self.piece_of_launch = tle_config["pieceOfLaunch"]
            self.year_of_launch = tle_config["launchYear"]

        self.element_number = element_number
        self.revolution_number = revolution_number
        self.__uni = uni
        self.__name = uuid4().hex

        """Initialize TLE from orbital parameters"""
        self.epoch = epoch

        # Convert to Keplerian elements
        pars = np.asarray(pars)
        kep = astro.convert("Equi", "Kep", pars[:-1], {"mu": uni.constants.getMu("Earth")})
        kep[1] = np.clip(kep[1], 0, 1)
        # Set elements
        self.ecc = kep[1]
        self.inc = kep[2]
        self.raan = num.wrapZero2Pi(kep[3])
        self.aop = num.wrapZero2Pi(kep[4])
        self.mean_anomaly = num.wrapZero2Pi(astro.meanFromTrue(kep[5], max(0, self.ecc)))

        # Compute mean motion (revs per day)
        self.mean_motion = 0.5 * tempo.SecondsInDay / math.pi * math.sqrt(uni.constants.getMu("Earth") / (kep[0] ** 3))

        # B* term
        self.bstar = pars[6]

        config = {
            "name": self.__name,
            "type": "PointTle",
            "config": {
                "origin": "Earth",
                "axes": "TEME",
                "tle": [self.to_line1(), self.to_line2()],
                "checkSum": True,
            },
        }
        uni.createPlugin("frames", [config])

    def to_line1(self) -> str:
        """Generate first line of TLE"""
        line = f"1 {self.norad_id:05d}{self.classification} "
        line += f"{self.year_of_launch % 100:02d}{self.launch_number:03d}{self.piece_of_launch:<3} "

        # Get day of year string from epoch
        doy_str = self.epoch.doyStr("UTC")  # Should return format like "2023-123"
        line += f"{doy_str[2:4]}{doy_str[5:8]}"  # Take YY and DDD parts

        # Get fraction of day from Julian Date
        jd = self.epoch.jd("UTC")
        fraction = jd - math.floor(jd)
        line += f"{fraction:.8f}"[1:]  # Skip the leading 0, keep 8 decimal places

        # Mean motion derivatives (set to 0)
        line += "  .00000000  00000+0 "

        # B* term
        line += self._bstar_string()

        # Element number and checksum
        line += f" 0 {self.element_number:4d}"
        line += str(self._checksum(line))

        return line

    def to_line2(self) -> str:
        """Generate second line of TLE"""
        line = f"2 {self.norad_id:05d} "
        line += f"{self.inc * 180/math.pi:8.4f} "
        line += f"{self.raan * 180/math.pi:8.4f} "

        # Eccentricity (decimal part only)
        line += f"{self.ecc:09.7f}"[2:]  # Skip "0."

        line += f" {self.aop * 180/math.pi:8.4f} "
        line += f"{self.mean_anomaly * 180/math.pi:8.4f} "
        line += f"{self.mean_motion:11.8f}"
        line += f"{self.revolution_number:5d}"
        line += str(self._checksum(line))

        return line

    def _bstar_string(self) -> str:
        """Format B* term for TLE"""
        bstar_zero_tol = 1e-9

        if abs(self.bstar) < bstar_zero_tol:
            return " 00000+0"
        if abs(self.bstar) < 1.0:
            bstar_str = f"{self.bstar:E}"
            mantissa, exponent = bstar_str.split("E")
            exponent_val = int(exponent) - 1
            num_str = f"{float(mantissa):+.4f}".replace(".", "")[0:5] + f"-{abs(exponent_val)}"
            return num_str if self.bstar < 0 else " " + num_str
        msg = f"B* value {self.bstar} exceeds maximum reasonable value."
        logger.error(msg)
        raise ValueError(msg)

    def _checksum(self, line: str) -> int:
        """Compute TLE line checksum"""
        sum_ = 0
        for c in line:
            if c.isdigit():
                sum_ += int(c)
            elif c == "-":
                sum_ += 1
        return sum_ % 10

    def eval(self, epoch: tempo.Epoch) -> NDArray:
        return self.__uni.frames.vector6("Earth", self.__name, "TEME", epoch)


def fit_tle_from_orbit(orbit: IpfOrbit, step: float) -> tuple[tempo.Epoch, str, str]:
    uni = cosmos.Universe(uni_config)
    try:
        ipf_point_name = orbit.id.hex

        uni.frames.addIpfPoint(ipf_point_name, "data/uploads/" + orbit.file_name, {3: "Earth"})

        blocks = uni.frames.blocks(uni.frames.pointId(ipf_point_name))

        fit_start, fit_end = blocks[0].range.start(), blocks[-1].range.end()
        logger.info(f"{fit_start}")
        logger.info(f"{fit_end}")
        fit_range = tempo.EpochRange(fit_start, fit_end)
        tle_epoch = fit_start

        kep_state = StateEqui(uni, ipf_point_name)
        kep_state.eval(tle_epoch)

        logger.info(uni.constants.getMu("Earth"))
        tle_variables = np.append(kep_state.eval(tle_epoch), 0.001)
        obs_epochs = fit_range.createGrid(step)
        obs = np.vstack([uni.frames.vector6("Earth", ipf_point_name, "TEME", e) for e in obs_epochs])
        tle_config: dict = orbit.satellite.tle_config
    except Exception:
        logger.exception("An error occurred during tle fitting.")
        raise
    return fit_tle(
        uni,
        tle_config=tle_config,
        tle_epoch=tle_epoch,
        initial_tle_variables=tle_variables,
        obs_epochs=obs_epochs,
        obs=obs,
    )


def fit_tle(
    uni: cosmos.Universe,
    tle_config: dict,
    tle_epoch: tempo.Epoch,
    initial_tle_variables: NDArray,
    obs_epochs: list,
    obs: NDArray,
    max_iter: int = 5,
    lm_damping_factor: float = 1e-3,
    coe_limit: bool = True,
) -> tuple[tempo.Epoch, str, str]:
    earth_radius = uni.constants.getRadius("Earth")
    earth_mu = uni.constants.getMu("Earth")

    initial_coe = initial_tle_variables
    original_a = np.asarray(initial_coe)[0]
    variances = np.array([1, 1, 1, 0.001, 0.001, 0.001])
    w = np.diag(1 / np.square(variances))
    variances[0:3] /= earth_radius
    variances[3:] /= np.sqrt(earth_mu / original_a)
    w_scaled = np.diag(1 / np.square(variances))

    b_scale = np.ones(6)
    b_scale[0:3] /= earth_radius
    b_scale[3:] /= np.sqrt(earth_mu / original_a)

    for iteration in range(max_iter):
        logger.info("TLE fitting iteration %s", iteration + 1)
        tle = TwoLineElement(uni, epoch=tle_epoch, pars=initial_coe, tle_config=tle_config)

        max_inner_iterations = 20  # Maximum iterations for the inner while loop
        inner_iteration = 0  # Counter for inner iterations

        while True:
            logger.info("TLE fitting inner iteration %s", inner_iteration + 1)
            residuals, jacobian = compute_residuals_and_jacobian(
                uni,
                tle,
                obs,
                obs_epochs,
                tle_epoch,
                initial_coe,
                earth_radius,
                earth_mu,
                original_a,
            )
            at_w_a = np.zeros((7, 7))
            at_w_b = np.zeros(7)

            for i_epoch in range(len(residuals)):
                at_w_a += jacobian[i_epoch].T @ w_scaled @ jacobian[i_epoch]
                at_w_b += jacobian[i_epoch].T @ w_scaled @ (residuals[i_epoch] * b_scale)

            pseudo_inverse = np.linalg.pinv(at_w_a + lm_damping_factor * at_w_a, hermitian=True)
            dx = pseudo_inverse @ at_w_b

            dx[0] *= earth_radius  # Rescale the first element
            logger.info("dx %s", dx)
            btwbs = residuals @ w @ residuals.T

            res_old = np.sum(btwbs) / 2

            new_els = initial_coe + dx

            new_els[6] = np.clip(new_els[6], -1, 1)  # Limit B*

            tle_new = TwoLineElement(uni, epoch=tle_epoch, pars=new_els, tle_config=tle_config)
            residuals_new = np.vstack([tle_new.eval(epoch) - ob for ob, epoch in zip(obs, obs_epochs, strict=False)])

            res_new = np.sum(residuals_new @ w @ residuals_new.T) / 2

            if res_new > res_old or np.isnan(res_new):
                lm_damping_factor *= 10
                inner_iteration += 1  # Increment inner iteration counter
                if inner_iteration >= max_inner_iterations:  # Check if max iterations reached
                    logger.warning("Inner loop exceeded maximum iterations, raising MaxIterationsExceededError.")
                    msg = "Maximum iterations exceeded during TLE fitting."
                    raise MaxIterationsExceededError(msg)
                continue
            lm_damping_factor = max(1e-3, lm_damping_factor / 10)
            break
        initial_coe += dx
        if coe_limit:
            initial_coe[1] = np.clip(initial_coe[1], 0, 1)  # Limit eccentricity
            initial_coe[6] = np.clip(initial_coe[6], -1, 1)  # Limit B*

        logger.info("Updated parameters: %s", initial_coe)
        logger.info("Residuals: %s", res_new)
    return tle_epoch, tle_new.to_line1(), tle_new.to_line2()


def compute_residuals_and_jacobian(
    uni: cosmos.Universe,
    tle: TwoLineElement,
    obs: NDArray,
    epochs: list[tempo.Epoch],
    tle_epoch: tempo.Epoch,
    tle_variables: NDArray,
    earth_radius: float,
    earth_mu: float,
    original_a: float,
) -> tuple[NDArray, NDArray]:
    """Compute residuals and the Jacobian matrix."""
    percent_chg = 1e-3
    residuals = np.vstack([ob - tle.eval(e) for ob, e in zip(obs, epochs, strict=False)])
    jacobian = np.zeros((len(epochs), 6, 7))  # Initialize the Jacobian matrix

    for idx, element in enumerate(tle_variables):
        variables_i = tle_variables.copy()
        delta_amt = 1e-08 if abs(element) < 1e-06 else element * percent_chg
        variables_i[idx] = element + delta_amt
        tle_plus = TwoLineElement(uni, epoch=tle_epoch, pars=variables_i)

        if idx == 0:
            delta_amt /= earth_radius

        for i_epoch, epoch_i in enumerate(epochs):
            res = tle_plus.eval(epoch_i) - tle.eval(epoch_i)
            jacobian[i_epoch, 0:3, idx] = res[:3] / earth_radius
            jacobian[i_epoch, 3:6, idx] = res[3:] / np.sqrt(earth_mu / original_a)
            jacobian[i_epoch, :, idx] /= delta_amt

    return residuals, jacobian
