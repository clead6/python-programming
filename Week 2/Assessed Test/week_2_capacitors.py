# -*- coding: utf-8 -*-

"""
PHYS20161 Week 2 quiz - Capactors

Lloyd Cawthorne 31/03/20

This code compares two calulations and then prints a statement accorindgly.
Correct 3 typos in the if-elif statements and then copy the output into
Blackboard.

This code compares two cylindrical capacitors with differing dielectric
material and size.
"""

#  import log function
import numpy as np

#  SI units

#  Constants

VACUUM_PERMITTIVITY = 8.54 * 10**-12

RELATIVE_PERMITTIVITY_AIR = 1.
RELATIVE_PERMITTIVITY_GLASS = 3.7


#  radius_1 is inner radius and radius_2 is outer radiuof
RADIUS_AIR_1 = 0.001
RADIUS_AIR_2 = 0.002

RADIUS_GLASS_1 = 0.001
RADIUS_GLASS_2 = 0.003


def capacitance_cylinder(radius_1, radius_2, relative_permittivity, length=1.):
    """ Returns the capacitance of a cylindrical capacitor (float). Use
    keyword argument to find total for given length, otherwise outputs per unit
    length.
    Args:
        radius_1 (float)
        radius_2 (float)
        relative_permittivity (float)
        length (float)
        """

    capacitance = ((2 * np.pi * VACUUM_PERMITTIVITY * relative_permittivity
                   * length) / (np.log(radius_2 / radius_1)))

    return capacitance


CAPACITANCE_AIR = capacitance_cylinder(RADIUS_AIR_1, RADIUS_AIR_2,
                                       RELATIVE_PERMITTIVITY_AIR)
CAPACITANCE_GLASS = capacitance_cylinder(RADIUS_GLASS_1, RADIUS_GLASS_2,
                                         RELATIVE_PERMITTIVITY_GLASS)

if CAPACITANCE_AIR > CAPACITANCE_GLASS:
    print("The capacitance per unit length of the air-filled capacitor is",
          CAPACITANCE_AIR / CAPACITANCE_GLASS,
          "times greater than the glass-filled capacitor.")

else:
    print("The capacitance per unit length of the glass-filled capacitor is",
          CAPACITANCE_GLASS / CAPACITANCE_AIR,
          "times greater than the air-filled capacitor.")
