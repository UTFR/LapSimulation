"""
Constants.py
"""

F_G = 9.81
WEIGHT_DIST = 0  # static weight dist 50-50%
COG_HEIGHT = 0.27
WHEEL_BASE = 1.6
FRONTAL_AREA = 1.25  # 0.98
MASS = 251.45
LAT_TIRE = 1.6
LONG_TIRE = 1
WHEEL_RADIUS = 0.229
AERO_BALANCE = 0.5
BRAKE_BIAS = 0.7
LIFT_COEF = 2.5  # this is also called CL
CD = 0  # drag coefficient --> 1.3

AIR_DENSITY = 1.225
GRAVITY = 9.81

GEAR_RATIOS = [2.071, 1.6250, 1.3330, 1.1200, .9630, 7.7605]

TORQUE_CURVE = [[3000, 3500, 4000, 4500, 5000, 5500, 6000, 6500, 7000, 7500, 8000, 8500, 9000, 9500, 10000, 10500],
                [27.4, 31.68, 35.99, 40.27, 44.5, 47.09, 46.08, 43.81, 41.53, 39.26, 36.98, 34.72, 32.44, 30.17, 27.89, 25.62]]

# I think these should go in the class of competition they correspond to
# Assuming these are data points to identify locations of straights and corners?
DATA_CORNER = [[26, 33, 24, 29, 20, 14, 35, 35, 24, 22, 19, 31, 30, 27, 35, 22, 35, 31, 25, 25, 27],
               [22, 6, 55, 8, 13, 2, 20, 6, 65, 9, 14, 13, 11, 14, 12, 10, 5, 5, 10, 10, 36],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


DATA_STRAIGHT = [[15, 116, 46, 22, 97, 41, 28, 13, 15, 9, 81, 5, 3, 98, 38, 94, 6, 9, 7, 12],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


