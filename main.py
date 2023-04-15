# import math
import threading
import time
# import numpy as np
from datetime import datetime

import pytz
# import matplotlib.pyplot as plt
from timezonefinder import TimezoneFinder


class SunPosition:
    def __init__(self):
        # Dependencies Date
        self.latitude = 0
        self.longitude = 0
        self.timezone = 0

        # Julian Values
        self.jd = 0
        self.jde = 0
        self.jc = 0
        self.jce = 0
        self.jme = 0

        # Dependencies Main
        self.year = 0
        self.month = 0
        self.day = 0
        self.hour = 0
        self.minute = 0
        self.second = 0
        self.day_decimal = None
        self.delta_t = 0
        self.utc_time = 0

    # Dependencies Date Get
    def get_timezone_and_utc(self):
        tf = TimezoneFinder()
        while True:
            # Importing Dependencies
            # Location
            latitude = self.latitude
            longitude = self.longitude

            utc_time = self.utc_time

            # Getting Timezone Area
            self.latitude = -23.326388680858557
            self.longitude = -51.20127294353894

            timezone = tf.timezone_at(lat=latitude, lng=longitude)
            # Exporting
            self.timezone = timezone

            if timezone != "Etc/GMT":
                utc_time = datetime.now(tz=pytz.UTC)
                # Exporting
                self.utc_time = utc_time

            if utc_time != 0:
                self.year = utc_time.year
                self.month = utc_time.month
                self.day = utc_time.day
                self.hour = utc_time.hour
                self.minute = utc_time.minute
                self.second = utc_time.second

            time.sleep(1)

    # Delta T and Julian Day and Julian Ephemeris Day
    def julian_day_and_ephemeris_day(self):
        while True:
            # Importing Dependencies
            year = self.year
            month = self.month
            day = self.day
            hour = self.hour
            minute = self.minute
            second = self.second
            day_decimal = self.day_decimal
            delta_t = self.delta_t
            utc_time = self.utc_time

            jd = self.jd
            jde = self.jde

            # Define day decimal:
            day_decimal = hour + minute / 60 + second / 3600


            if year and month and day_decimal != 0:
                # Calculating delta_t
                t = (year - 1820) / 100
                delta_t = 62.92 + 0.32217 * t + 0.005589 * t ** 2

                # Calculating Julian Day
                jd = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day_decimal - 1524.5

                # Calculating Julian Ephemeris Day
                jde = jd + (delta_t / 86400)

                # Exporting
                self.delta_t = delta_t
                self.jd = jd
                self.jde = jde

            time.sleep(1)


# Julian Century and Julian Ephemeris Century and Julian Ephemeris Millennium
    def julian_century_and_ephemeris_century_and_ephemeris_millennium(self):
        while True:
            #Importing dependencies
            jd = self.jd
            jde = self.jde

            jc = self.jc
            jce = self.jce
            jme = self.jme

            if jd and jde != 0:
                # Calculating Julian Century
                jc = (jd - 2451545) / 36525

                # Calculating Julian Ephemeris Century
                jce = (jde - 2451545) / 36525

                # Exporting
                self.jc = jc
                self.jce = jce

                if jce != 0:
                    # Calculating Julian Ephemeris Millenniun
                    jme = jce / 10

                    # Exporting
                    self.jme = jme

            time.sleep(1)


# MultiThreading
sun_position = SunPosition()

get_timezone_thread = threading.Thread(target=sun_position.get_timezone_and_utc)
get_timezone_thread.start()

julian_day_and_ephemeris_day_thread = threading.Thread(target=sun_position.julian_day_and_ephemeris_day)
julian_day_and_ephemeris_day_thread.start()

julian_century_and_ephemeris_century_and_ephemeris_millennium_thread = threading.Thread(target=sun_position.julian_century_and_ephemeris_century_and_ephemeris_millennium)
julian_century_and_ephemeris_century_and_ephemeris_millennium_thread.start()
