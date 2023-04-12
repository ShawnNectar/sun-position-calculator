import math
import threading
import time
from datetime import datetime

import numpy as np
import pytz
from timezonefinder import TimezoneFinder

hidden_from_streamlit = """
╔══════════════════════════════════════════════╗
║                   IMPORTANT                  ║
║                                              ║
║ Julian Day                                   ║
║   JD = INT(365.25*(Y + 4716)) +              ║
║        INT(30.6001*(M + 1)) + D + B - 1524.5 ║
║                                              ║
║ Julian Century                               ║
║   JC = (JD - 2451545) / 36525                ║
║                                              ║          
║ Julian Ephemeris Day                         ║
║                                              ║         
║   JDE = JD + (ΔT / 86400)                    ║
║ Julian Ephemeris Century                     ║
║   JCE = (JDE - 2451545) / 36525              ║
║                                              ║
║ Julian Ephemeris Century                     ║
║     JCE = (JDE - 2451545) / 36525            ║
║                                              ║
║ Julian Ephemeris Millennium                  ║
║   JME = JCE/10                               ║
║                                              ║
║ Earth heliocentric longitude, latitude, and  ║
║ radius vector (L, B, R)                      ║
║   L0i = Ai * cos(Bi + Ci * JME)              ║
║                                              ║
║ Earth Heliocentric Longitude (radians)       ║
║     L = (L0 + L1 * JME + L2 * JME^2 + L3 * \ ║
║     JME^3 + L4 * JME^4 + L5 * JME^5) / 10^8  ║
║                                              ║                
║ L in Degrees                                 ║                 
║     Ld = (L * 180) / pi                      ║     
║                                              ║
║ Geocentric Longitude (degrees)               ║
║     Geo_Lat = L + 180                        ║
║                                              ║
║ Geocentric Latitude (degrees)                ║
║     Geo_Lat = - B                            ║     
║                                              ║
╚══════════════════════════════════════════════╝
Geocentric Longitude (degrees)
Geo_Lat = L + 180
"""


class SunPosition:
    def __init__(self):
        periodic_terms_L0 = (
            (0, 175347046, 0, 0),
            (1, 3341656, 4.6692568, 6283.07585),
            (2, 34894, 4.6261, 12566.1517),
            (3, 3497, 2.7441, 5753.3849),
            (4, 3418, 2.8289, 3.5231),
            (5, 3136, 3.6277, 77713.7715),
            (6, 2676, 4.4181, 7860.4194),
            (7, 2343, 6.1352, 3930.2097),
            (8, 1324, 0.7425, 11506.7698),
            (9, 1273, 2.0371, 529.691),
            (10, 1199, 1.1096, 1577.3435),
            (11, 990, 5.233, 5884.927),
            (12, 902, 2.045, 26.298),
            (13, 857, 3.508, 398.149),
            (14, 780, 1.179, 5223.694),
            (15, 753, 2.533, 5507.553),
            (16, 505, 4.583, 18849.228),
            (17, 492, 4.205, 775.523),
            (18, 357, 2.92, 0.067),
            (19, 317, 5.849, 11790.629),
            (20, 284, 1.899, 796.298),
            (21, 271, 0.315, 10977.079),
            (22, 243, 0.345, 5486.778),
            (23, 206, 4.806, 2544.314),
            (24, 205, 1.869, 5573.143),
            (25, 202, 2.458, 6069.777),
            (26, 156, 0.833, 213.299),
            (27, 132, 3.411, 2942.463),
            (28, 126, 1.083, 20.775),
            (29, 115, 0.645, 0.98),
            (30, 103, 0.636, 4694.003),
            (31, 102, 0.976, 15720.839),
            (32, 102, 4.267, 7.114),
            (33, 99, 6.21, 2146.17),
            (34, 98, 0.68, 155.42),
            (35, 86, 5.98, 161000.69),
            (36, 85, 1.3, 6275.96),
            (37, 85, 3.67, 71430.7),
            (38, 80, 1.81, 17260.15),
            (39, 79, 3.04, 12036.46),
            (40, 75, 1.76, 5088.63),
            (41, 74, 3.5, 3154.69),
            (42, 74, 4.68, 801.82),
            (43, 70, 0.83, 9437.76),
            (44, 62, 3.98, 8827.39),
            (45, 61, 1.82, 7084.9),
            (46, 57, 2.78, 6286.6),
            (47, 56, 4.39, 14143.5),
            (48, 56, 3.47, 6279.55),
            (49, 52, 0.19, 12139.55),
            (50, 52, 1.33, 1748.02),
            (51, 51, 0.28, 5856.48),
            (52, 49, 0.49, 1194.45),
            (53, 41, 5.37, 8429.24),
            (54, 41, 2.4, 19651.05),
            (55, 39, 6.17, 10447.39),
            (56, 37, 6.04, 10213.29),
            (57, 37, 2.57, 1059.38),
            (58, 36, 1.71, 2352.87),
            (59, 36, 1.78, 6812.77),
            (60, 33, 0.59, 17789.85),
            (61, 30, 0.44, 83996.85),
            (62, 30, 2.74, 1349.87),
            (63, 25, 3.16, 4690.48),
        )

        periodic_terms_L1 = (
            (0, 628331966747, 0, 0),
            (1, 206059, 2.678235, 6283.07585),
            (2, 4303, 2.6351, 12566.1517),
            (3, 425, 1.59, 3.523),
            (4, 119, 5.796, 26.298),
            (5, 109, 2.966, 1577.344),
            (6, 93, 2.59, 18849.23),
            (7, 72, 1.14, 529.69),
            (8, 68, 1.87, 398.15),
            (9, 67, 4.41, 5507.55),
            (10, 59, 2.89, 5223.69),
            (11, 56, 2.17, 155.42),
            (12, 45, 0.4, 796.3),
            (13, 36, 0.47, 775.52),
            (14, 29, 2.65, 7.11),
            (15, 21, 5.34, 0.98),
            (16, 19, 1.85, 5486.78),
            (17, 19, 4.97, 213.3),
            (18, 17, 2.99, 6275.96),
            (19, 16, 0.03, 2544.31),
            (20, 16, 1.43, 2146.17),
            (21, 15, 1.21, 10977.08),
            (22, 12, 2.83, 1748.02),
            (23, 12, 3.26, 5088.63),
            (24, 12, 5.27, 1194.45),
            (25, 12, 2.08, 4694),
            (26, 11, 0.77, 553.57),
            (27, 10, 1.3, 6286.6),
            (28, 10, 4.24, 1349.87),
            (29, 9, 2.7, 242.73),
            (30, 9, 5.64, 951.72),
            (31, 8, 5.3, 2352.87),
            (32, 6, 2.65, 9437.76),
            (33, 6, 4.67, 4690.48),
        )

        periodic_terms_L2 = (
            (0, 52919, 0, 0),
            (1, 8720, 1.0721, 6283.0758),
            (2, 309, 0.867, 12566.152),
            (3, 27, 0.05, 3.52),
            (4, 16, 5.19, 26.3),
            (5, 16, 3.68, 155.42),
            (6, 10, 0.76, 18849.23),
            (7, 9, 2.06, 77713.77),
            (8, 7, 0.83, 775.52),
            (9, 5, 4.66, 1577.34),
            (10, 4, 1.03, 7.11),
            (11, 4, 3.44, 5573.14),
            (12, 3, 5.14, 796.3),
            (13, 3, 6.05, 5507.55),
            (14, 3, 1.19, 242.73),
            (15, 3, 6.12, 529.69),
            (16, 3, 0.31, 398.15),
            (17, 3, 2.28, 553.57),
            (18, 2, 4.38, 5223.69),
            (19, 2, 3.75, 0.98),
        )

        periodic_terms_L3 = (
            (0, 289, 5.844, 6283.076),
            (1, 35, 0, 0),
            (2, 17, 5.49, 12566.15),
            (3, 3, 5.2, 155.42),
            (4, 1, 4.72, 3.52),
            (5, 1, 5.3, 18849.23),
            (6, 1, 5.97, 242.73),
        )

        periodic_terms_L4 = (
            (0, 114, 3.142, 0),
            (1, 8, 4.13, 6283.08),
            (2, 1, 3.84, 12566.15),
        )

        periodic_terms_L5 = (
            (0, 1, 3.14, 0)
        )

        periodic_terms_B0 = (
            (0, 280, 3.199, 84334.662),
            (1, 102, 5.422, 5507.553),
            (2, 80, 3.88, 5223.69),
            (3, 44, 3.7, 2352.87),
            (4, 32, 4, 1577.34),
        )

        periodic_terms_B1 = (
            (0, 9, 3.9, 5507.55),
            (1, 6, 1.73, 5223.69))

        periodic_terms_R0 = (
            (0, 100013989, 0, 0),
            (1, 1670700, 3.0984635, 6283.07585),
            (2, 13956, 3.05525, 12566.1517),
            (3, 3084, 5.1985, 77713.7715),
            (4, 1628, 1.1739, 5753.3849),
            (5, 1576, 2.8469, 7860.4194),
            (6, 925, 5.453, 11506.77),
            (7, 542, 4.564, 3930.21),
            (8, 472, 3.661, 5884.927),
            (9, 346, 0.964, 5507.553),
            (10, 329, 5.9, 5223.694),
            (11, 307, 0.299, 5573.143),
            (12, 243, 4.273, 11790.629),
            (13, 212, 5.847, 1577.344),
            (14, 186, 5.022, 10977.079),
            (15, 175, 3.012, 18849.228),
            (16, 110, 5.055, 5486.778),
            (17, 98, 0.89, 6069.78),
            (18, 86, 5.69, 15720.84),
            (19, 86, 1.27, 161000.69),
            (20, 65, 0.27, 17260.15),
            (21, 63, 0.92, 529.69),
            (22, 57, 2.01, 83996.85),
            (23, 56, 5.24, 71430.7),
            (24, 49, 3.25, 2544.31),
            (25, 47, 2.58, 775.52),
            (26, 45, 5.54, 9437.76),
            (27, 43, 6.01, 6275.96),
            (28, 39, 5.36, 4694),
            (29, 38, 2.39, 8827.39),
            (30, 37, 0.83, 19651.05),
            (31, 37, 4.9, 12139.55),
            (32, 36, 1.67, 12036.46),
            (33, 35, 1.84, 2942.46),
            (34, 33, 0.24, 7084.9),
            (35, 32, 0.18, 5088.63),
            (36, 32, 1.78, 398.15),
            (37, 28, 1.21, 6286.6),
            (38, 28, 1.9, 6279.55),
            (39, 26, 4.59, 10447.39),
        )

        periodic_terms_R1 = (
            (0, 103019, 1.10749, 6283.07585),
            (1, 1721, 1.0644, 12566.1517),
            (2, 702, 3.142, 0),
            (3, 32, 1.02, 18849.23),
            (4, 31, 2.84, 5507.55),
            (5, 25, 1.32, 5223.69),
            (6, 18, 1.42, 1577.34),
            (7, 10, 5.91, 10977.08),
            (8, 9, 1.42, 6275.96),
            (9, 9, 0.27, 5486.78),
        )

        periodic_terms_R2 = (
            (0, 4359, 5.7846, 6283.0758),
            (1, 124, 5.579, 12566.152),
            (2, 12, 3.14, 0),
            (3, 9, 3.63, 77713.77),
            (4, 6, 1.87, 5573.14),
            (5, 3, 5.47, 18849.23),
        )

        periodic_terms_R3 = ((0, 145, 4.273, 6283.076), (1, 7, 3.92, 12566.15))

        periodic_terms_R4 = (1, 4, 2.56, 6283.08) # 0 to 1

        self.terms_L0 = periodic_terms_L0
        self.terms_L1 = periodic_terms_L1
        self.terms_L2 = periodic_terms_L2
        self.terms_L3 = periodic_terms_L3
        self.terms_L4 = periodic_terms_L4
        self.terms_L5 = periodic_terms_L5

        self.terms_B0 = periodic_terms_B0
        self.terms_B1 = periodic_terms_B1

        self.terms_R0 = periodic_terms_R0
        self.terms_R1 = periodic_terms_R1
        self.terms_R2 = periodic_terms_R2
        self.terms_R3 = periodic_terms_R3
        self.terms_R4 = periodic_terms_R4

        self.julian_day = None
        self.julian_century = None
        self.julian_ephemeris_day = None
        self.julian_ephemeris_century = None
        self.julian_ephemeris_millennium = None

        self.sum_L0 = None
        self.sum_L1 = None
        self.sum_L0 = None
        self.sum_L1 = None
        self.sum_L2 = None
        self.sum_L3 = None
        self.sum_L4 = None
        self.sum_L5 = None
        self.sum_B0 = None
        self.sum_B1 = None
        self.sum_R0 = None
        self.sum_R1 = None
        self.sum_R2 = None
        self.sum_R3 = None
        self.sum_R4 = None

        self.latitude = -23.326388680858557
        self.longitude = -51.20127294353894
        self.timezone = None
        self.time_utc = None

    def timezone_utc_and_julian_day(self):
        tf = TimezoneFinder()
        while True:
            latitude = self.latitude
            longitude = self.longitude
            timezone = tf.timezone_at(lat=latitude, lng=longitude)
            self.timezone = timezone

            utc_time = datetime.now(tz=pytz.UTC)

            year = utc_time.year
            month = utc_time.month
            day = utc_time.day
            hour = utc_time.hour
            minute = utc_time.minute
            second = utc_time.second

            decimal_hours = hour + minute / 60 + second / 3600

            julian_day = np.add(
                np.add(
                    np.add(
                        np.multiply(365.25, np.add(year, 4716)),
                        np.multiply(30.6001, np.add(month, 1)),
                    ),
                    day,
                ),
                decimal_hours,
            )
            self.julian_day = julian_day

            time.sleep(1)

    def julian_century_and_epoch(self):
        while True:
            julian_day = self.julian_day
            if julian_day is not None:
                julian_century = np.divide(np.subtract(julian_day, 2451545), 36525)
                self.julian_century = julian_century

            time.sleep(1)

    def julian_ephemeris_day_and_century(self):
        while True:
            julian_day = self.julian_day
            if julian_day is not None:
                julian_ephemeris_day = julian_day + (37 / 86400)

                julian_ephemeris_century = (julian_ephemeris_day - 2451545) / 36525

                self.julian_ephemeris_century = julian_ephemeris_century
                self.julian_ephemeris_day = julian_ephemeris_day

            time.sleep(1)

    def julian_ephemeris_millennium_func(self):
        while True:
            julian_ephemeris_century = self.julian_ephemeris_century
            if julian_ephemeris_century is not None:
                julian_ephemeris_millennium = julian_ephemeris_century / 10

                self.julian_ephemeris_millennium = julian_ephemeris_millennium

            time.sleep(1)

    def earth_periodic_terms_sum(self):
        while True:
            terms_L0 = self.terms_L0
            terms_L1 = self.terms_L1
            terms_L2 = self.terms_L2
            terms_L3 = self.terms_L3
            terms_L4 = self.terms_L4
            terms_L5 = self.terms_L5

            terms_B0 = self.terms_B0
            terms_B1 = self.terms_B1

            terms_R0 = self.terms_R0
            terms_R1 = self.terms_R1
            terms_R2 = self.terms_R2
            terms_R3 = self.terms_R3
            terms_R4 = self.terms_R4
            julian_ephemeris_millennium = self.julian_ephemeris_millennium
            (
                sum_L0,
                sum_L1,
                sum_L2,
                sum_L3,
                sum_L4,
                sum_L5,
                sum_B0,
                sum_B1,
                sum_R0,
                sum_R1,
                sum_R2,
                sum_R3,
                sum_R4,
            ) = (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

            if julian_ephemeris_millennium is not None:

                for i in range(len(terms_L0)):
                    sum_L0 += terms_L0[i][0] * math.cos(
                        terms_L0[i][1] + terms_L0[i][2] * julian_ephemeris_millennium
                    )

                    self.sum_L0 = sum_L0

                for i in range(len(terms_L1)):
                    sum_L1 += terms_L1[i][0] * math.cos(
                        terms_L1[i][1] + terms_L1[i][2] * julian_ephemeris_millennium
                    )

                    self.sum_L1 = sum_L1
                for i in range(len(terms_L2)):
                    sum_L2 += terms_L2[i][0] * math.cos(
                        terms_L2[i][1] + terms_L2[i][2] * julian_ephemeris_millennium
                    )

                    self.sum_L2 = sum_L2

                for i in range(len(terms_L3)):
                    sum_L3 += terms_L3[i][0] * math.cos(
                        terms_L3[i][1] + terms_L3[i][2] * julian_ephemeris_millennium
                    )

                    self.sum_L3 = sum_L3
                for i in range(len(terms_L4)):
                    sum_L4 += terms_L4[i][0] * math.cos(
                        terms_L4[i][1] + terms_L4[i][2] * julian_ephemeris_millennium
                    )

                    self.sum_L4 = sum_L4

                for i in range(1):
                    sum_L5 += 1 * math.cos(
                        3.14 + 0 * julian_ephemeris_millennium
                    )

                    self.sum_L5 = sum_L5

                for i in range(len(terms_B0)):
                    sum_B0 += terms_B0[i][0] * math.cos(
                        terms_B0[i][1] + terms_B0[i][2] * julian_ephemeris_millennium
                    )

                    self.sum_B0 = sum_B0




            time.sleep(1)

    def show_all_values(self):
        while True:
            julian_day = self.julian_day
            julian_century = self.julian_century
            julian_ephemeris_day = self.julian_ephemeris_day
            julian_ephemeris_century = self.julian_ephemeris_century
            julian_ephemeris_millennium = self.julian_ephemeris_millennium
            sum_L0 = self.sum_L0
            sum_L1 = self.sum_L1
            sum_L2 = self.sum_L2
            sum_L3 = self.sum_L3
            sum_L4 = self.sum_L4
            sum_L5 = self.sum_L5

            sum_B0 = self.sum_B0
            sum_B1 = self.sum_B1

            sum_R0 = self.sum_R0
            sum_R1 = self.sum_R1
            sum_R2 = self.sum_R2
            sum_R3 = self.sum_R3
            sum_R4 = self.sum_R4

            if (
                    julian_day
                    and julian_century
                    and julian_ephemeris_day
                    and julian_ephemeris_century
                    and julian_ephemeris_millennium
                    and sum_L0
                    and sum_L1
                    and sum_L2
                    and sum_L3
                    and sum_L4
                    and sum_L5
                    is not None
            ):
                print("Values: ")
                print(f"Julian Day: {julian_day}")
                print(f"Julian Century: {julian_century}")

                print("")

                print(f"Julian Ephemeris Day: {julian_ephemeris_day}")
                print(f"Julian Ephemeris Century: {julian_ephemeris_century}")

                print("")

                print(f"Julian Ephemeris Millennium: {julian_ephemeris_millennium}")

                print(f"Sum of L0: {sum_L0}")
                print(f"Sum of L1: {sum_L1}")
                print(f"Sum of L2: {sum_L2}")
                print(f"Sum of L3: {sum_L3}")
                print(f"Sum of L4: {sum_L4}")
                print(f"Sum of L5: {sum_L5}")
                print(f"Sum of B0: {sum_B0}")

            time.sleep(1)


sun_position = SunPosition()

julian_day_thread = threading.Thread(target=sun_position.timezone_utc_and_julian_day)
julian_day_thread.start()

julian_century_thread = threading.Thread(target=sun_position.julian_century_and_epoch)
julian_century_thread.start()

julian_ephemeris_day_thread = threading.Thread(
    target=sun_position.julian_ephemeris_day_and_century
)
julian_ephemeris_day_thread.start()

julian_ephemeris_millennium_thread = threading.Thread(
    target=sun_position.julian_ephemeris_millennium_func
)
julian_ephemeris_millennium_thread.start()

earth_periodic_terms_sum_thread = threading.Thread(
    target=sun_position.earth_periodic_terms_sum
)
earth_periodic_terms_sum_thread.start()

show_all_values_thread = threading.Thread(target=sun_position.show_all_values)
show_all_values_thread.start()