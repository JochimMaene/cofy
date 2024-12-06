from io import BytesIO

import numpy as np
import pandas as pd
from godot.core import ipfwrap, tempo


def update_leap_second_data(response, file_name: str) -> None:
    with open("data/" + file_name, "wb") as file:
        file.write(response.content)


def back_ground_space_weather(response, file_name: str) -> None:
    space_weather_ipf_from_cssi(BytesIO(response.content), "data/" + file_name)


def back_ground_eop(response, file_name: str) -> None:
    erp_ipf_from_iers(BytesIO(response.content), "data/" + file_name)


def download_JPL_ephemeris(response, file_name: str) -> None:
    with open("data/" + file_name, "wb") as file:
        file.write(response.content)


def space_weather_ipf_from_cssi(input_csv: str | BytesIO, output_file: str):
    """Write a space weather ipf file from cssi space weather data.
    The space weather ipf file is needed by GODOT to use the NRLMSISE-00 atmospheric model.
    However, GODOT provides no functionality to produce these files. This function takes the space
    weather data in .csv format as can be found on Celestrak [1]_ and converts it in the ipf
    format.

    Parameters
    ----------
    input_csv : str
        the space weather input file, must be a csv file
    output_file : str
        the file and path where the ipf file shall be sorted, e.g. /data/space_weather.ipf

    Notes
    -----
    The daily f10.7 and averaged, centered f10.7 values take the observed and not the adjusted
    values as expected by the NRLMSISE-00 model. [2]_

    References
    ----------
    .. [1] https://celestrak.org/SpaceData/
    .. [2] https://forum.orekit.org/t/cssispaceweatherdata-java-using-adjusted-and-not-observed-flux-values/1290

    See also
    --------
    space_weather_ipf_from_msfc
    """
    sw_data = pd.read_csv(input_csv)

    sw_data.DATE = [tempo.Epoch(x.strftime("%Y-%m-%d") + " TT").mjd() for x in pd.to_datetime(sw_data.DATE)]
    writer = ipfwrap.IpfWriter(output_file, 3, 0, 20)
    writer.newBlock()
    for _, x in sw_data.iterrows():
        writer.put(x["DATE"], [x["F10.7_OBS"], x["F10.7_OBS_CENTER81"], x["AP_AVG"]])
    del writer


def erp_ipf_from_iers(input_file: str | BytesIO, output_file: str):
    """Write an ERP correction ipf file from IERS IAU2000 data [1]_. The data must be given as a
    csv file. The latest csv can be directly download using the link below [2]_. Without the ERP
    file, GODOT uses an approximate method such that the Earth orientation is valid within about
    15 arcseconds.

    Parameters
    ----------
    input_file : str
        the IERS input file, must be a csv file
    output_file : str
        the file and path where the ipf file shall be sorted

    References
    ----------
    .. [1] https://www.iers.org/IERS/EN/DataProducts/EarthOrientationData/eop.html
    .. [2] https://datacenter.iers.org/data/csv/finals2000A.data.csv

    Note
    ----
    This function uses with the Bulletain A and Bulletin B data. Whenever, Bulletin B data (= the
    standard solution) is available, this is used. Bulletin A data is used otherwise, providing
    data for the recent past and predictions for the future.

    """

    #  data format is given here:https://maia.usno.navy.mil/ser7/readme.finals2000A

    iers_data = pd.read_csv(input_file, delimiter=";")

    # ipf polar motion and corrects are expected in radians
    arcsec_to_rad = np.pi / 180 / 3600

    iers_data[["pmx", "pmy"]] = (
        iers_data[["bulB/x_pole", "bulB/y_pole"]].fillna(iers_data[["x_pole", "y_pole"]]) * arcsec_to_rad
    )
    iers_data[["pmdx", "pmdy"]] = (
        iers_data[["bulB/dX", "bulB/dY"]].fillna(iers_data[["dX", "dY"]]).fillna(0) * arcsec_to_rad / 1e3
    )

    # ipf time key is expected in TT
    iers_data["mjd_TT"] = iers_data.MJD.apply(lambda x: tempo.Epoch(str(x) + " MJD TT").mjd())
    iers_data["mjd_UTC"] = iers_data.MJD.apply(lambda x: tempo.Epoch(str(x) + " MJD UTC").mjd())
    iers_data["UT1-TT"] = (
        iers_data["bulB/UT-UTC"].fillna(iers_data["UT1-UTC"]) / 86400 + iers_data.mjd_TT - iers_data.mjd_UTC
    )

    writer = ipfwrap.IpfWriter(
        filename=output_file,
        dimension=5,
        derivatives=0,
        fileType=1,
        blockHeaderSize=12,
        fileHeader=[0, 0, 0, 0, 0, 0, 0, 0],
    )
    writer.newBlock([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    for _, x in iers_data.iterrows():
        writer.put(x["mjd_TT"], [x["pmx"], x["pmy"], x["UT1-TT"], x["pmdx"], x["pmdy"]])