Environment files
=================

The environment files contain necessary data to perform the flight dynamics computations. These include for example the ephemeris files, Earth orientation parameters and space weather data. The files are not provided with the application, but are automatically downloaded and stored in the `/data` folder next to the application. The data can be automatically updated at configurable intervals to ensure that always the latest data is being used. An update of all environment files also happens at startup of the application. To keep track of the status of each environement file, an SQL table is used which contains information such as the updating frequency or whether a file is out-of-date.

To schedule the times at which the data is periodically updated, a [cron expression](https://en.wikipedia.org/wiki/Cron) is used. The default cron expression is `0 2 * * *`, which schedules the updates every day at 2 AM UTC. Each environement file also has an unique integer value id associated to it, to keep track of the status of the files in a SQL table. The id can also be used to change the update settings for each file. The following environment files, with their id are inserted as default in the database:



| id  | Name                         | Description        | Cron      | URL                                                       |
| --- | ---------------------------- | ------------------ | --------- | --------------------------------------------------------- |
| 1   | Leap seconds                 |                    | 0 2 * * * | https://astroutils.astronomy.osu.edu/time/tai-utc.txt     |
| 2   | Space weather                | CSSI space weather | 0 2 * * * | https://celestrak.org/SpaceData/SW-Last5Years.csv         |
| 3   | Earth orientation parameters |                    | 0 2 * * * | https://datacenter.iers.org/data/csv/finals2000A.data.csv |
| 4   | JPL ephermeris               |                    | null      | https://ssd.jpl.nasa.gov/ftp/eph/planets/bsp/de440s.bsp   |


If the cron expression is left empty, the data will not be updated periodically.
The files are always overwritten when they are updated. If you want to maintain an archive, the files can be downloaded.
