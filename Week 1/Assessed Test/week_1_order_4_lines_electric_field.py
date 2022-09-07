# -*- coding: utf-8 -*-

"""

PHYS20161 Week 1 - Electric Field

The lines of code below are correct, however they are in the wrong order.
Correct the order then submit the correct order to Blackboard
(e.g. "A, B, C, D" or "C, B, A, D").

Lloyd Cawthorne 18/02/19

"""

# SI units

print('The magnitude of the electric field experienced by the charge is ',
      ELECTRIC_FIELD, ' V/m')  # line A
ELECTRIC_FIELD = FORCE / CHARGE  # line B
FORCE = 0.5  # line C
CHARGE = 2 * pow(10, -2)  # line D
