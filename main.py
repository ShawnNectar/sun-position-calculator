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
        
        
"""


class JulianDayCalculations:
    def __init__(self):
        self.julian_day = None

    # Julian Day and UTC and Timezone
    def timezone_utc_and_julian_day(self):
        # Get timezone and UTC time from user's coordinates // UTC time
        tf = TimezoneFinder()
        while True:
            latitude = -23.326388680858557
            longitude = -51.20127294353894
            timezone = tf.timezone_at(lat=latitude, lng=longitude)

            # Get UTC time
            utc_time = datetime.now(tz=pytz.UTC)
            print(timezone)
            print(utc_time)

            # It's self explanatory
            year = utc_time.year
            month = utc_time.month
            day = utc_time.day
            hour = utc_time.hour
            minute = utc_time.minute
            second = utc_time.second

            decimal_hours = hour + minute / 60 + second / 3600

            # Applying the JD = INT(365.25*(Y + 4716)) + INT(30.6001*(M + 1)) + D + B - 1524.5 from NREL
            julian_day = (
                int(365.25 * (year + 4716))
                + int(30.6001 * (month + 1))
                + day
                + decimal_hours
            )

            self.julian_day = julian_day
            print(f"Julian Day: {julian_day}")

            time.sleep(5)


# Julian Century
class JulianCenturyCalculations:
    def __init__(self, jdc):
        self.jdc = jdc

    def julian_century_and_epoch(self):
        while True:
            julian_day = self.jdc.julian_day
            if julian_day is not None:
                # Applying the JC = (JD - 2451545) / 36525 from NREL
                julian_century = (julian_day - 2451545) / 36525
                print(f"Julian Century: {julian_century}")

            time.sleep(5)


class geometricMeanLongitudeSunCalculations:
    def __init__(self, jdc, jcc):
        self.jdc = jdc
        self.jcc = jcc

    def mean_longitude(self):
        while True:
            julian_day = self.jdc.julian_day
            julian_century = self.jcc.julian_century
            if julian_day is not None and julian_century is not None:
                # Applying GMST0 = 280.46061837 + 360.98564736629 * (JD - 2451545.0) + 0.000387933 * JC * JC - (JC * JC * JC) / 38710000.0
                GMST0 = (
                    280.46061837
                    + 360.98564736629 * (julian_day - 2451545.0)
                    + 0.000387933 * julian_century * julian_century
                    - (julian_century * julian_century * julian_century) / 38710000.0
                )
                print(f"GMST0: {GMST0}")


jdc = JulianDayCalculations()
julian_day_thread = threading.Thread(target=jdc.timezone_utc_and_julian_day)
julian_day_thread.start()

jcc = JulianCenturyCalculations(jdc)
julian_century_thread = threading.Thread(target=jcc.julian_century_and_epoch)
julian_century_thread.start()

gmls = geometricMeanLongitudeSunCalculations(jdc, jcc)
gmls_thread = threading.Thread(target=gmls.mean_longitude)
gmls_thread.start()


# Geometric Mean Longitude of the Sun (GMST0)

# Geometric Mean Anomaly of the Sun (GMSA)

# Equation of Center (EC)

# True Longitude of the Sun (TLS)

# The Apparent Longitude of the Sun (ALS)

# Obliquity of the Ecliptic (OE)

# Right Ascension of the Sun (RAS)

# Declination of the Sun (DS)

# Greenwich Mean Sidereal Time (GMST)

# Local Mean Sidereal Time (LMST)
