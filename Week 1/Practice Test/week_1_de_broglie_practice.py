# -*- coding: utf-8 -*-
"""
Order 4 lines of code

Practice version for PHYS20161 week 1 quiz

Lloyd Cawthorne 28/08/19

The code below calculates the de Broglie wavelength given a momentum.
However the lines are in an incorrect order.
Correct the order then select the answer on BlackBoard.
"""

# SI units

print('The particle has a wavelength of', WAVELENGTH, ' m.')  # line A
MOMENTUM = 5.0 * 10**-27  # line B
WAVELENGTH = PLANCK_CONSTANT / MOMENTUM  # line C
PLANCK_CONSTANT = 6.626 * 10**-34  # line D
