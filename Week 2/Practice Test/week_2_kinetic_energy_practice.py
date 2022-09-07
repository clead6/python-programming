# -*- coding: utf-8 -*-
"""
PHYS20161 week 2 - Kinetic energy

This code caclulates the kinetic energy of a 5.7 kg mass given its velocity.

It contains 3 bugs you need to correct. Once it is working, use 62.8299431 m/s
as the velocity and copy the answer into BB.

Lloyd Cawthorne - 13/09/19

"""

# SI Units

MASS = 5.7

VELOCITY = float(input('What is the velocity of the mass in m/s?' ))
KINETIC_ENERGY = 0.5 * MASS * VELOCITY**2
print('The object has a kinetic energy of ', KINETIC_ENERGY, 'J.')
