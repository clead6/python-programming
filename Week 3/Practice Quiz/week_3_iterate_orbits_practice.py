# -*- coding: utf-8 -*-
"""
PHYS20161 week 3 practice quiz iterate orbits

This code finds and prints the period of a planet (in days) given its distance
to the Sun (in AU).

Assumed circular orbits in each case.

Correct four errors then select the appropriate answers on BlackBoard.

Lloyd Cawthorne 24/09/19

"""
# Constants

KEPLER_CONSTANT = 7.5 * 10**-6

PLANET_DATA = [['Mercury', 0.38710], ['Venus', 0.72333], ['Earth', 1.],
               ['Mars',	1.52366], ['Jupiter', 5.20336], ['Saturn', 9.53707],
               ['Uranus', 19.1913], ['Neptune', 30.0690]]

# Declare an empty array with the same length as 'planet_data'
PLANET_PERIODS = [0] * len(PLANET_DATA)

for i in range(len(PLANET_DATA)):
    # Overwrite each element of areas with desired calculation
    PLANET_PERIODS[i] = ((PLANET_DATA[i][1]**3) / (KEPLER_CONSTANT))**0.5
    print('The period of {0:^7} is {1:5.0f} days.'.format(PLANET_DATA[i][0], PLANET_PERIODS[i]))
    
print(PLANET_DATA[3])
