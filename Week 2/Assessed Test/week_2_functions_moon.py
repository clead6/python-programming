# -*- coding: utf-8 -*-

"""
PHYS20161 Week 2: functions Moon

Debug the three mistakes in the code below.
Once it works, copy the output into Blackboard.

Lloyd Cawthorne 18/02/19
"""

import numpy as np

# S.I. units

GRAVITATIONAL_CONSTANT = 6.67 * pow(10, -11)
MASS_MOON = 7.35 * 10**22
MASS_EARTH = 5.97 * pow(10, 24)
MOON_ORBIT_RADIUS = 385000000


def gravitational_force_newton(mass_1, mass_2, radius):
    """Returns gravitational force (float) according to Newton's formula
    Args:
        mass_1 (float)
        mass_2 (float)
        radius (float)
    """

    gravitational_force = (GRAVITATIONAL_CONSTANT * mass_1 * mass_2
                           / pow(radius, 2))

    return gravitational_force


def velocity_centripetal(force, mass, radius):
    """Returns velocity from centripetal force (float)
    Args:
        force (float)
        mass (float)
        radius (float)
    """

    velocity = np.sqrt(radius * force / mass)

    return velocity


VELOCITY = velocity_centripetal(gravitational_force_newton(MASS_MOON,
                                                           MASS_EARTH,
                                                           MOON_ORBIT_RADIUS),
                                MASS_MOON, MOON_ORBIT_RADIUS)

print('The velocity of the Moon orbiting the Earth is', VELOCITY, 'm/s.')
