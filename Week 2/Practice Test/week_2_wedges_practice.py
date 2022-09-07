# -*- coding: utf-8 -*-
"""
PHYS20161 - Week 2 Debug 3 errors if-elif wedge

This code compares the resultant magnitudes of the acceleration of identical
masses on different frictional wedges.

Correct three bugs in the if-elif-else statements then copy the output into
BlackBoard.


Lloyd Cawthorne 13/09/19

"""

# import trig functions

import numpy as np

# SI units

# Properties of wedges

WEDGE_ANGLE_1 = 30.0
COEFFICIENT_OF_FRICTION_1 = 0.5

WEDGE_ANGLE_2 = 25.0
COEFFICIENT_OF_FRICTION_2 = 0.4

# constant

G_CONSTANT = 6.67 * pow(10, -11)


def resultant_acceleration(wedge_angle, coefficient_of_friction):
    """Returns the magnitude of the resultant acceleration for a mass on a
    wedge given the angle and coefficient of friction that define the wedge.

    Form found by equaitng Newton 2 to resultant force on the inclined plane.

    wedge_angle, degrees (float)
    coefficient_of_friction (float)
    """
    # convert degree to rad
    wedge_angle_rad = wedge_angle * np.pi / 180.0

    acceleration = (1.0 / G_CONSTANT) * (np.sin(wedge_angle_rad)
                                         - coefficient_of_friction
                                         * np.cos(wedge_angle_rad))
    return acceleration


ACCELERATION_ON_WEDGE_1 = resultant_acceleration(WEDGE_ANGLE_1,
                                                 COEFFICIENT_OF_FRICTION_1)
ACCELERATION_ON_WEDGE_2 = resultant_acceleration(WEDGE_ANGLE_2,
                                                 COEFFICIENT_OF_FRICTION_2)

if ACCELERATION_ON_WEDGE_1 > ACCELERATION_ON_WEDGE_2:
    print('The mass accelerates',
          ACCELERATION_ON_WEDGE_1 / ACCELERATION_ON_WEDGE_2,
          'times more on the wedge 1 than wedge 2.')
else:
    print('The mass accelerates',
          ACCELERATION_ON_WEDGE_2 / ACCELERATION_ON_WEDGE_1,
          'times more one the wedge 2 than wedge 1.')
