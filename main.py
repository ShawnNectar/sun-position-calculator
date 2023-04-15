# import math
import time
import pytz
import threading

# import numpy as np
from datetime import datetime
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

        # Dependencies Main
        self.year = 0
        self.month = 0
        self.day = 0
        self.minute = 0
        self.second = 0
        self.day_decimal = 0
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

                print(utc_time)

            time.sleep(1)


# Julian Day and Julian Ephemeris Day

# Julian Century and Julian Ephemeris Century and Julian Ephemeris Millennium


# MultiThreading
sun_position = SunPosition()
get_timezone_thread = threading.Thread(target=sun_position.get_timezone_and_utc)
get_timezone_thread.start()