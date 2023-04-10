import datetime
import numpy as np
import pytz
import streamlit as st
from timezonefinder import TimezoneFinder
import time
from datetime import datetime

hidden_from_streamlit = '''
        IMPORTANT
        
Julian Day
    JD = 2451545.0 + (Current Time UTC - 12:00:00) / 24.0

Julian Century
    JC = (JD - 2451545.0) / 36525.0

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
        
        
'''
# Get timezone and UTC time from user's coordinates

# Julian Day temporary****it's going to be updated to inputs in a couple hours

year = 2023
month = 4
day = 10
hours = 12
minutes = 30
seconds = 30

decimal_hours = hours + minutes/60 + seconds/3600

julian_day = int(365.25*(year+4716)) + int(30.6001*(month+1)) + day+decimal_hours

print(decimal_hours)
print(julian_day)

# Julian Century

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
