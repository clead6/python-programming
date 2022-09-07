# -*- coding: utf-8 -*-
"""
PHYS20161 week 3 quiz iterate waves

This code finds and prints the angle of refraction for light incident on
water given a series of incident angles.

All angles in degrees w.r.t. normal.

Correct three errors then select the appropriate answers on BlackBoard.

Lloyd Cawthorne 24/09/19

"""

# import trig functions

import numpy as np

# SI units

REFRACTION_INDEX_WATER = 1.333

DEGREE_TO_RADIAN = np.pi / 180.

INCIDENT_ANGLES = [0.0, 15.6, 20.34, 30.2, 41.7, 48.9, 50.06, 65.3, 76.]


def refracted_angle(incident_angle):
    """
    Calculates refracted angle from air to water as per Snell's law (float)

    incident_angle (float, degrees)

    All angles converted to degrees
    """
    theta_2 = np.arcsin(np.sin(incident_angle * DEGREE_TO_RADIAN)
                        / REFRACTION_INDEX_WATER) / DEGREE_TO_RADIAN

    return theta_2


#  Declare an empty array with the same length as 'INCIDENT_ANGLES'
REFRACTED_ANGLES = [0] * len(INCIDENT_ANGLES)

for i in range(len(INCIDENT_ANGLES)):

    # Overwrite each element of REFRACTED_ANGLES with desired calculation
    REFRACTED_ANGLES[i] = refracted_angle(INCIDENT_ANGLES[i])

    print('Light incident at {0:4.2f} degrees is refracted to {1:4.2f}'
          ' degrees.'.format(INCIDENT_ANGLES[i], REFRACTED_ANGLES[i]))
    
print(REFRACTED_ANGLES[7])
