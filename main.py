import threading
import time
from datetime import datetime #, tzinfo

# import numpy as np
import pytz
# import streamlit as st
from timezonefinder import TimezoneFinder

hidden_from_streamlit = """
        IMPORTANT
        
Julian Day
    JD = INT(365.25*(Y + 4716)) + INT(30.6001*(M + 1)) + D + B - 1524.5
Julian Century
    JC = (JD - 2451545) / 36525
Geometric Mean Longitude of the Sun (GMST0)
    GMST0 = 280.46061837 + 360.98564736629 * (JD - 2451545.0) + 0.000387933 * JC * JC - (JC * JC * JC) / 38710000.0
Geometric Mean Anomaly of the Sun (GMSA)
    GMSA = 357.52911 + JC * (35999.05029 - 0.0001537 * JC)
Equation of Center (EC)
    EC = (1.914602 - JC * (0.004817 + 0.000014 * JC)) * sin(GMSA) + (0.019993 - 0.000101 * JC) * sin(2 * GMSA) + 0.00029 * sin(3 * GMSA)
True Longitude of the Sun (TLS)
    TLS = GMST0 + GMSA + EC
The Apparent Longitude of the Sun (ALS)
    ALS = TLS - 0.00569 - 0.00478 * sin(125.04 - 1934.136 * JC)
Obliquity of the Ecliptic (OE)
    OE = 23.439291 - 0.0130042 * JC - 0.00000016 * JC * JC + 0.000000504 * JC * JC * JC
Right Ascension of the Sun (RAS)
    RAS = atan2(cos(OE) * sin(ALS), cos(ALS))
Declination of the Sun (DS)
    DS = asin(sin(OE) * sin(ALS))
Greenwich Mean Sidereal Time (GMST)
    GMST = GMST0 + 360.98564736629 * (current time in UTC - 12:00:00) / 24.0
Local Mean Sidereal Time (LMST)
    LMST = GMST + observer's longitude / 15.0
        
        MAY CHANGE TO NPEL PATTERN 
        
"""


class SunPosition:
    def __init__(self):
        self.julian_day = None
        self.julian_century = None

    def timezone_utc_and_julian_day(self):
        tf = TimezoneFinder()
        while True:
            latitude = -23.326388680858557
            longitude = -51.20127294353894
            timezone = tf.timezone_at(lat=latitude, lng=longitude)

            utc_time = datetime.now(tz=pytz.UTC)
            print(timezone)
            print(utc_time)

            year = utc_time.year
            month = utc_time.month
            day = utc_time.day
            hour = utc_time.hour
            minute = utc_time.minute
            second = utc_time.second

            decimal_hours = hour + minute / 60 + second / 3600

            julian_day = (
                    int(365.25 * (year + 4716))
                    + int(30.6001 * (month + 1))
                    + day
                    + decimal_hours
            )

            self.julian_day = julian_day
            print(f"Julian Day: {julian_day}")

            time.sleep(5)

    def julian_century_and_epoch(self):
        while True:
            julian_day = self.julian_day
            if julian_day is not None:
                julian_century = (julian_day - 2451545) / 36525
                self.julian_century = julian_century
                print(f"Julian Century: {julian_century}")

            time.sleep(5)

    def mean_longitude(self):
        while True:
            julian_day = self.julian_day
            julian_century = self.julian_century
            if julian_day is not None and julian_century is not None:
                GMST0 = (
                        280.46061837
                        + 360.98564736629 * (julian_day - 2451545.0)
                        + 0.000387933 * julian_century * julian_century
                        - (julian_century * julian_century * julian_century) / 38710000.0
                )
                print(f"GMST0: {GMST0}")

            time.sleep(5)


sun_position = SunPosition()

julian_day_thread = threading.Thread(target=sun_position.timezone_utc_and_julian_day)
julian_day_thread.start()

julian_century_thread = threading.Thread(target=sun_position.julian_century_and_epoch)
julian_century_thread.start()

mean_longitude_thread = threading.Thread(target=sun_position.mean_longitude)
mean_longitude_thread.start()

