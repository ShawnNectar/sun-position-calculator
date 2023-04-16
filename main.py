# import math
import threading
import time
from datetime import datetime

import numpy as np
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

        # Main
        self.heliocentric_longitude = 0
        self.heliocentric_latitude = 0
        self.heliocentric_position_radius = 0

        self.geocentric_longitude = 0
        self.geocentric_latitude = 0

        self.X0 = 0
        self.X1 = 0
        self.X2 = 0
        self.X3 = 0
        self.X4 = 0

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
            self.latitude = -23.326388680858557 # Reference Latitude
            self.longitude = -51.20127294353894 # Reference Longitude

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
            hour = self.hour
            minute = self.minute
            second = self.second

            # Define day decimal:
            day_decimal = hour + minute / 60 + second / 3600

            if year and month and day_decimal != 0:
                # Calculating delta_t
                t = (year - 1820) / 100
                delta_t = 62.92 + 0.32217 * t + 0.005589 * t ** 2

                # Calculating Julian Day
                jd = (
                        int(365.25 * (year + 4716))
                        + int(30.6001 * (month + 1))
                        + day_decimal
                        - 1524.5
                )

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
            # Importing dependencies
            jd = self.jd
            jde = self.jde

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

    # Earth Heliocentric Longitude
    def earth_heliocentric_longitude(self):
        # Data Dependencies From Tables
        L0_terms = np.array(
            [
                [1.75347046e08, 0.00000000e00, 0.00000000e00],
                [3.34165600e06, 4.66925680e00, 6.28307585e03],
                [3.48940000e04, 4.62610000e00, 1.25661517e04],
                [3.49700000e03, 2.74410000e00, 5.75338490e03],
                [3.41800000e03, 2.82890000e00, 3.52310000e00],
                [3.13600000e03, 3.62770000e00, 7.77137715e04],
                [2.67600000e03, 4.41810000e00, 7.86041940e03],
                [2.34300000e03, 6.13520000e00, 3.93020970e03],
                [1.32400000e03, 7.42500000e-01, 1.15067698e04],
                [1.27300000e03, 2.03710000e00, 5.29691000e02],
                [1.19900000e03, 1.10960000e00, 1.57734350e03],
                [9.90000000e02, 5.23300000e00, 5.88492700e03],
                [9.02000000e02, 2.04500000e00, 2.62980000e01],
                [8.57000000e02, 3.50800000e00, 3.98149000e02],
                [7.80000000e02, 1.17900000e00, 5.22369400e03],
                [7.53000000e02, 2.53300000e00, 5.50755300e03],
                [5.05000000e02, 4.58300000e00, 1.88492280e04],
                [4.92000000e02, 4.20500000e00, 7.75523000e02],
                [3.57000000e02, 2.92000000e00, 6.70000000e-02],
                [3.17000000e02, 5.84900000e00, 1.17906290e04],
                [2.84000000e02, 1.89900000e00, 7.96298000e02],
                [2.71000000e02, 3.15000000e-01, 1.09770790e04],
                [2.43000000e02, 3.45000000e-01, 5.48677800e03],
                [2.06000000e02, 4.80600000e00, 2.54431400e03],
                [2.05000000e02, 1.86900000e00, 5.57314300e03],
                [2.02000000e02, 2.44580000e00, 6.06977700e03],
                [1.56000000e02, 8.33000000e-01, 2.13299000e02],
                [1.32000000e02, 3.41100000e00, 2.94246300e03],
                [1.26000000e02, 1.08300000e00, 2.07750000e01],
                [1.15000000e02, 6.45000000e-01, 9.80000000e-01],
                [1.03000000e02, 6.36000000e-01, 4.69400300e03],
                [1.02000000e02, 9.76000000e-01, 1.57208390e04],
                [1.02000000e02, 4.26700000e00, 7.11400000e00],
                [9.90000000e01, 6.21000000e00, 2.14617000e03],
                [9.80000000e01, 6.80000000e-01, 1.55420000e02],
                [8.60000000e01, 5.98000000e00, 1.61000690e05],
                [8.50000000e01, 1.30000000e00, 6.27596000e03],
                [8.50000000e01, 3.67000000e00, 7.14307000e04],
                [8.00000000e01, 1.81000000e00, 1.72601500e04],
                [7.90000000e01, 3.04000000e00, 1.20364600e04],
                [7.10000000e01, 1.76000000e00, 5.08863000e03],
                [7.40000000e01, 3.50000000e00, 3.15469000e03],
                [7.40000000e01, 4.68000000e00, 8.01820000e02],
                [7.00000000e01, 8.30000000e-01, 9.43776000e03],
                [6.20000000e01, 3.98000000e00, 8.82739000e03],
                [6.10000000e01, 1.82000000e00, 7.08490000e03],
                [5.70000000e01, 2.78000000e00, 6.28660000e03],
                [5.60000000e01, 4.39000000e00, 1.41435000e04],
                [5.60000000e01, 3.47000000e00, 6.27955000e03],
                [5.20000000e01, 1.90000000e-01, 1.21395500e04],
                [5.20000000e01, 1.33000000e00, 1.74802000e03],
                [5.10000000e01, 2.80000000e-01, 5.85648000e03],
                [4.90000000e01, 4.90000000e-01, 1.19445000e03],
                [4.10000000e01, 5.37000000e00, 8.42924000e03],
                [4.10000000e01, 2.40000000e00, 1.96510500e04],
                [3.90000000e01, 6.17000000e00, 1.04473900e04],
                [3.70000000e01, 6.04000000e00, 1.02132900e04],
                [3.70000000e01, 2.57000000e00, 1.05938000e03],
                [3.60000000e01, 1.71000000e00, 2.35287000e03],
                [3.60000000e01, 1.78000000e00, 6.81277000e03],
                [3.30000000e01, 5.90000000e-01, 1.77898500e04],
                [3.00000000e01, 4.40000000e-01, 8.39968500e04],
                [3.00000000e01, 2.74000000e00, 1.34987000e03],
                [2.50000000e01, 3.16000000e00, 4.69048000e03],
            ]
        )

        L1_terms = np.array(
            [
                [6.28331967e11, 0.00000000e00, 0.00000000e00],
                [2.06059000e05, 2.67823500e00, 6.28307585e03],
                [4.30300000e03, 2.63510000e00, 1.25661517e04],
                [4.25000000e02, 1.59000000e00, 3.52300000e00],
                [1.19000000e02, 5.79600000e00, 2.62980000e01],
                [1.09000000e02, 2.96600000e00, 1.57734400e03],
                [9.30000000e01, 2.59000000e00, 1.88492300e04],
                [7.20000000e01, 1.14000000e00, 5.29690000e02],
                [6.80000000e01, 1.87000000e00, 3.98150000e02],
                [6.70000000e01, 4.41000000e00, 5.50755000e03],
                [5.90000000e01, 2.89000000e00, 5.22369000e03],
                [5.60000000e01, 2.17000000e00, 1.55420000e02],
                [4.50000000e01, 4.00000000e-01, 7.96300000e02],
                [3.60000000e01, 4.70000000e-01, 7.75520000e02],
                [2.90000000e01, 2.65000000e00, 7.11000000e00],
                [2.10000000e01, 5.34000000e00, 9.80000000e-01],
                [1.90000000e01, 1.85000000e00, 5.48678000e03],
                [1.90000000e01, 4.97000000e00, 2.13300000e02],
                [1.70000000e01, 2.99000000e00, 6.27596000e03],
                [1.60000000e01, 3.00000000e-02, 2.54431000e03],
                [1.60000000e01, 1.43000000e00, 2.14617000e03],
                [1.50000000e01, 1.21000000e00, 1.09770800e04],
                [1.20000000e01, 2.83000000e00, 1.74802000e03],
                [1.20000000e01, 3.26000000e00, 5.08863000e03],
                [1.20000000e01, 5.27000000e00, 1.19445000e03],
                [1.20000000e01, 2.08000000e00, 4.69400000e03],
                [1.10000000e01, 7.70000000e-01, 5.53570000e02],
                [1.00000000e01, 1.30000000e00, 3.28660000e03],
                [1.00000000e01, 4.24000000e00, 1.34987000e03],
                [9.00000000e00, 2.70000000e00, 2.42730000e02],
                [9.00000000e00, 5.64000000e00, 9.51720000e02],
                [8.00000000e00, 5.30000000e00, 2.35287000e03],
                [6.00000000e00, 2.65000000e00, 9.43776000e03],
                [6.00000000e00, 4.67000000e00, 4.69048000e03],
            ]
        )
        L2_terms = np.array(
            [
                [5.2919000e04, 0.0000000e00, 0.0000000e00],
                [8.7200000e03, 1.0721000e00, 6.2830758e03],
                [3.0900000e02, 8.6700000e-01, 1.2566152e04],
                [2.7000000e01, 5.0000000e-02, 3.5200000e00],
                [1.6000000e01, 5.1900000e00, 2.6300000e01],
                [1.6000000e01, 3.6800000e00, 1.5542000e02],
                [1.0000000e01, 7.6000000e-01, 1.8849230e04],
                [9.0000000e00, 2.0600000e00, 7.7713770e04],
                [7.0000000e00, 8.3000000e-01, 7.7552000e02],
                [5.0000000e00, 4.6600000e00, 1.5773400e03],
                [4.0000000e00, 1.0300000e00, 7.1100000e00],
                [4.0000000e00, 3.4400000e00, 5.5731400e03],
                [3.0000000e00, 5.1400000e00, 7.9630000e02],
                [3.0000000e00, 6.0500000e00, 5.5075500e03],
                [3.0000000e00, 1.1900000e00, 2.4273000e02],
                [3.0000000e00, 6.1200000e00, 5.2969000e02],
                [3.0000000e00, 3.1000000e-01, 3.9815000e02],
                [3.0000000e00, 2.2800000e00, 5.5357000e02],
                [2.0000000e00, 4.3800000e00, 5.2236900e03],
                [2.0000000e00, 3.7500000e00, 9.8000000e-01],
            ]
        )
        L3_terms = np.array(
            [
                [2.890000e02, 5.844000e00, 6.283076e03],
                [3.500000e01, 0.000000e00, 0.000000e00],
                [1.700000e01, 5.490000e00, 1.256615e04],
                [3.000000e00, 5.200000e00, 1.554200e02],
                [1.000000e00, 4.720000e00, 3.520000e00],
                [1.000000e00, 5.300000e00, 1.884923e04],
                [1.000000e00, 5.970000e00, 2.427300e02],
            ]
        )
        L4_terms = np.array(
            [
                [1.140000e02, 3.142000e00, 0.000000e00],
                [8.000000e00, 4.130000e00, 6.283080e03],
                [1.000000e00, 3.840000e00, 1.256615e04],
            ]
        )
        L5_terms = np.array([[1, 3.14, 0]])

        A0POS = L0_terms[:, 0]
        B0POS = L0_terms[:, 1]
        C0POS = L0_terms[:, 2]

        A1POS = L1_terms[:, 0]
        B1POS = L1_terms[:, 1]
        C1POS = L1_terms[:, 2]

        A2POS = L2_terms[:, 0]
        B2POS = L2_terms[:, 1]
        C2POS = L2_terms[:, 2]

        A3POS = L3_terms[:, 0]
        B3POS = L3_terms[:, 1]
        C3POS = L3_terms[:, 2]

        A4POS = L4_terms[:, 0]
        B4POS = L4_terms[:, 1]
        C4POS = L4_terms[:, 2]

        A5POS = L5_terms[:, 0]
        B5POS = L5_terms[:, 1]
        C5POS = L5_terms[:, 2]
        while True:
            # Importing Dependencies
            jme = self.jme
            if jme != 0:
                L0_sum = np.sum(A0POS * np.cos(B0POS + (C0POS * jme)))
                L1_sum = np.sum(A1POS * np.cos(B1POS + (C1POS * jme)))
                L2_sum = np.sum(A2POS * np.cos(B2POS + (C2POS * jme)))
                L3_sum = np.sum(A3POS * np.cos(B3POS + (C3POS * jme)))
                L4_sum = np.sum(A4POS * np.cos(B4POS + (C4POS * jme)))
                L5_sum = np.sum(A5POS * np.cos(B5POS + (C5POS * jme)))

                heliocentric_longitude = (
                                                 L0_sum
                                                 + (L1_sum * jme)
                                                 + (L2_sum * jme ** 2)
                                                 + (L3_sum * jme ** 3)
                                                 + (L4_sum * jme ** 4)
                                                 + (L5_sum * jme ** 5)
                                         ) / 1e8
                heliocentric_longitude = heliocentric_longitude * 180 / np.pi
                heliocentric_longitude %= 360

                # Exporting
                self.heliocentric_longitude = heliocentric_longitude

            time.sleep(1)

    def earth_heliocentric_latitude(self):
        # Data Dependencies From Tables
        B0_terms = np.array(
            [
                [2.8000000e02, 3.1990000e00, 8.4334662e04],
                [1.0200000e02, 5.4220000e00, 5.5075530e03],
                [8.0000000e01, 3.8800000e00, 5.2236900e03],
                [4.4000000e01, 3.7000000e00, 2.3528700e03],
                [3.2000000e01, 4.0000000e00, 1.5773400e03],
            ]
        )

        B1_terms = np.array(
            [[9.00000e00, 3.90000e00, 5.50755e03], [6.00000e00, 1.73000e00, 5.22369e03]]
        )

        A0POS = B0_terms[:, 0]
        B0POS = B0_terms[:, 1]
        C0POS = B0_terms[:, 2]

        A1POS = B1_terms[:, 0]
        B1POS = B1_terms[:, 1]
        C1POS = B1_terms[:, 2]

        while True:
            # Importing Dependencies
            jme = self.jme

            if jme != 0:
                L0_sum = np.sum(A0POS * np.cos(B0POS + (C0POS * jme)))
                L1_sum = np.sum(A1POS * np.cos(B1POS + (C1POS * jme)))

                heliocentric_latitude = (L0_sum + (L1_sum * jme)) / 1e8
                heliocentric_latitude = heliocentric_latitude * 180 / np.pi
                heliocentric_latitude %= 360

                # Exporting
                self.heliocentric_latitude = heliocentric_latitude
            time.sleep(1)

    def earth_heliocentric_position_radius(self):
        # Data Dependencies From Tables
        R0_terms = np.array(
            [
                [1.00013989e08, 0.00000000e00, 0.00000000e00],
                [1.67070000e06, 3.09846350e00, 6.28307585e03],
                [1.39560000e04, 3.05525000e00, 1.25661517e04],
                [3.08400000e03, 5.19850000e00, 7.77137715e04],
                [1.62800000e03, 1.17390000e00, 5.75338490e03],
                [1.57600000e03, 2.84690000e00, 7.86041940e03],
                [9.25000000e02, 5.45300000e00, 1.15067700e04],
                [5.42000000e02, 4.56400000e00, 3.93021000e03],
                [4.72000000e02, 3.66100000e00, 5.88492700e03],
                [3.46000000e02, 9.64000000e-01, 5.50755300e03],
                [3.29000000e02, 5.90000000e00, 5.22369400e03],
                [3.07000000e02, 2.99000000e-01, 5.57314300e03],
                [2.43000000e02, 4.27300000e00, 1.17906290e04],
                [2.12000000e02, 5.84700000e00, 1.57734400e03],
                [1.86000000e02, 5.02200000e00, 1.09770790e04],
                [1.75000000e02, 3.01200000e00, 1.88492280e04],
                [1.10000000e02, 5.05500000e00, 5.48677800e03],
                [9.80000000e01, 8.90000000e-01, 6.06978000e03],
                [8.60000000e01, 5.69000000e00, 1.57208400e04],
                [8.60000000e01, 1.27000000e00, 1.61000690e05],
                [8.50000000e01, 2.70000000e-01, 1.72601500e04],
                [6.30000000e01, 9.20000000e-01, 5.29690000e02],
                [5.70000000e01, 2.01000000e00, 8.39968500e04],
                [5.60000000e01, 5.24000000e00, 7.14307000e04],
                [4.90000000e01, 3.25000000e00, 2.54431000e03],
                [4.70000000e01, 2.58000000e00, 7.75520000e02],
                [4.50000000e01, 5.54000000e00, 9.43776000e03],
                [4.30000000e01, 6.01000000e00, 6.27596000e03],
                [3.90000000e01, 5.36000000e00, 4.69400000e03],
                [3.80000000e01, 2.39000000e00, 8.82739000e03],
                [3.70000000e01, 8.30000000e-01, 1.96510500e04],
                [3.70000000e01, 4.90000000e00, 1.21395500e04],
                [3.60000000e01, 1.67000000e00, 1.20364600e04],
                [3.50000000e01, 1.84000000e00, 2.94246000e03],
                [3.30000000e01, 2.40000000e-01, 7.08490000e03],
                [3.20000000e01, 1.80000000e-01, 5.08863000e03],
                [3.20000000e01, 1.78000000e00, 3.98150000e02],
                [2.80000000e01, 1.21000000e00, 6.28660000e03],
                [2.80000000e01, 1.90000000e00, 6.27955000e03],
                [2.60000000e01, 4.59000000e00, 1.04473900e04],
            ]
        )

        R1_terms = np.array(
            [
                [1.03019000e05, 1.10749000e00, 6.28307585e03],
                [1.72100000e03, 1.06440000e00, 1.25661517e04],
                [7.02000000e02, 3.14200000e00, 0.00000000e00],
                [3.20000000e01, 1.02000000e00, 1.88492300e04],
                [3.10000000e01, 2.84000000e00, 5.50755000e03],
                [2.50000000e01, 1.32000000e00, 5.22369000e03],
                [1.80000000e01, 1.42000000e00, 1.57734000e03],
                [1.00000000e01, 5.91000000e00, 1.09770800e04],
                [9.00000000e00, 1.42000000e00, 6.27596000e03],
                [9.00000000e00, 2.70000000e-01, 5.48678000e03],
            ]
        )

        R2_terms = np.array(
            [
                [4.3590000e03, 5.7846000e00, 6.2830758e03],
                [1.2400000e02, 5.5790000e00, 1.2566152e04],
                [1.2000000e01, 3.1400000e00, 0.0000000e00],
                [9.0000000e00, 3.6300000e00, 7.7713770e04],
                [6.0000000e00, 1.8700000e00, 5.5731400e03],
                [3.0000000e00, 5.4700000e00, 1.8849000e04],
            ]
        )

        R3_terms = np.array(
            [
                [1.450000e02, 4.273000e00, 6.283076e03],
                [7.000000e00, 3.920000e00, 1.256615e04],
            ]
        )

        R4_terms = np.array([4.00000e00, 2.56000e00, 6.28308e03])

        A0POS = R0_terms[:, 0]
        B0POS = R0_terms[:, 1]
        C0POS = R0_terms[:, 2]

        A1POS = R1_terms[:, 0]
        B1POS = R1_terms[:, 1]
        C1POS = R1_terms[:, 2]

        A2POS = R2_terms[:, 0]
        B2POS = R2_terms[:, 1]
        C2POS = R2_terms[:, 2]

        A3POS = R3_terms[:, 0]
        B3POS = R3_terms[:, 1]
        C3POS = R3_terms[:, 2]

        A4POS = R4_terms[0]
        B4POS = R4_terms[1]
        C4POS = R4_terms[2]

        while True:
            # Importing Dependencies
            jme = self.jme

            if jme != 0:
                L0_sum = np.sum(A0POS * np.cos(B0POS + (C0POS * jme)))
                L1_sum = np.sum(A1POS * np.cos(B1POS + (C1POS * jme)))
                L2_sum = np.sum(A2POS * np.cos(B2POS + (C2POS * jme)))
                L3_sum = np.sum(A3POS * np.cos(B3POS + (C3POS * jme)))
                L4_sum = np.sum(A4POS * np.cos(B4POS + (C4POS * jme)))

                heliocentric_position_radius = (
                                                       L0_sum
                                                       + (L1_sum * jme)
                                                       + (L2_sum * jme ** 2)
                                                       + (L3_sum * jme ** 3)
                                                       + (L4_sum * jme ** 4)
                                               ) / 1e8

                # Exporting
                self.heliocentric_position_radius = heliocentric_position_radius
            time.sleep(1)

    def sun_geocentric_longitude_and_latitude(self):
        while True:
            # Importing Dependenciesv
            heliocentric_longitude = self.heliocentric_longitude
            heliocentric_latitude = self.heliocentric_latitude

            if heliocentric_longitude and heliocentric_latitude != 0:
                # Calculating Geocentric Longitude
                geocentric_longitude = heliocentric_longitude + 180
                geocentric_longitude %= 360

                # Calculating Geocentric Latitude
                geocentric_latitude = -heliocentric_latitude
                geocentric_latitude %= 360

                # Exporting
                self.geocentric_longitude = geocentric_longitude
                self.geocentric_latitude = geocentric_latitude
            time.sleep(1)

    def nutation_in_longitude_and_obliquity(self):
        while True:
            # Importing Dependencies
            jce = self.jce

            if jce != 0:
                # Calculating Mean Elongation of Moon from Sun (X0)
                X0 = 297.85036 + 445267.111480 * jce - 0.0019142 * jce**2 + jce**3 / 189474
                # Calculating mean anomaly of the sun (X1)
                X1 = 357.52772 + 35999.050340 * jce - 0.0001603 * jce**2 - jce**3 / 300000
                # Calculating Mean Anomaly of the Moon (X2)
                X2 = 134.96298 + 477198.867398 * jce - 0.0086972 * jce**2 + jce**3 / 56250
                # Calculating Moon's Argument of Latitude (X3)
                X3 = 93.27191 + 483202.017538 * jce - 0.0036825 * jce**2 + jce**3 / 327270
                # Calculating Longitude of Ascending Node of Moon's mean Orbit on the Ecliptic
                X4 = 125.04452 - 1934.136261 * jce + 0.0020708 * jce**2 + jce**3 / 450000


                self.X0 = X0
                self.X1 = X1
                self.X2 = X2
                self.X3 = X3
                self.X4 = X4

            time.sleep(1)

    def show_all_values(self):
        while True:
            """
            # Dependencies Date
            latitude = self.latitude
            longitude = self.longitude
            timezone = self.timezone

            # Julian Values
            jd = self.jd
            jde = self.jde
            jc = self.jc
            jce = self.jce
            jme = self.jme

            # Dependencies Main
            year = self.year
            month = self.month
            day = self.day
            hour = self.hour
            minute = self.minute
            second = self.second
            day_decimal = self.day_decimal
            delta_t = self.delta_t
            utc_time = self.utc_time
            """

            # Main
            heliocentric_longitude = self.heliocentric_longitude
            heliocentric_latitude = self.heliocentric_latitude
            heliocentric_position_radius = self.heliocentric_position_radius

            geocentric_longitude = self.geocentric_longitude
            geocentric_latitude = self.geocentric_latitude

            X0 = self.X0
            X1 = self.X1
            X2 = self.X2
            X3 = self.X3
            X4 = self.X4

            if (
                    heliocentric_longitude
                    and heliocentric_latitude
                    and heliocentric_position_radius
                    and geocentric_longitude
                    and geocentric_latitude
                    and X0
                    and X1
                    and X2
                    and X3
                    and X4 != 0
            ):
                print("Values: ")
                print(f"Heliocentric Longitude: {heliocentric_longitude}°")
                print(f"Heliocentric Latitude: {heliocentric_latitude}°")
                print(f"Heliocentric Position Radius: {heliocentric_position_radius}°")
                print(f"Geocentric Longitude: {geocentric_longitude}°")
                print(f"Geocentric Latitude: {geocentric_latitude}°")

                print(f"Mean Elongation of Moon from Sun: {X0}°")
                print(f"Mean Anomaly of the Sun: {X1}°")
                print(f"Mean Anomaly of the Moon: {X2}°")
                print(f"Moon's Argument of Latitude: {X3}°")
                print(f"Ascending Node Moon's Mean Orbit Longitude Ecliptic: {X4}°")


                time.sleep(1)
            time.sleep(1)


# MultiThreading
sun_position = SunPosition()

get_timezone_thread = threading.Thread(target=sun_position.get_timezone_and_utc)
get_timezone_thread.start()

julian_day_and_ephemeris_day_thread = threading.Thread(
    target=sun_position.julian_day_and_ephemeris_day
)
julian_day_and_ephemeris_day_thread.start()

julian_century_and_ephemeris_century_and_ephemeris_millennium_thread = threading.Thread(
    target=sun_position.julian_century_and_ephemeris_century_and_ephemeris_millennium
)
julian_century_and_ephemeris_century_and_ephemeris_millennium_thread.start()

earth_heliocentric_longitude_thread = threading.Thread(
    target=sun_position.earth_heliocentric_longitude
)
earth_heliocentric_longitude_thread.start()

earth_heliocentric_latitude_thread = threading.Thread(
    target=sun_position.earth_heliocentric_latitude
)
earth_heliocentric_latitude_thread.start()

earth_heliocentric_position_radius_thread = threading.Thread(
    target=sun_position.earth_heliocentric_position_radius
)
earth_heliocentric_position_radius_thread.start()

sun_geocentric_longitude_and_latitude_thread = threading.Thread(
    target=sun_position.sun_geocentric_longitude_and_latitude
)
sun_geocentric_longitude_and_latitude_thread.start()

nutation_in_longitude_and_obliquity_thread = threading.Thread(target=sun_position.nutation_in_longitude_and_obliquity)
nutation_in_longitude_and_obliquity_thread.start()

show_all_values_thread = threading.Thread(target=sun_position.show_all_values)
show_all_values_thread.start()
