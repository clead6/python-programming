# -*- coding: utf-8 -*-
"""
PHYS20161 week 2 rotation speed

The code below is presented in the correct order, however,
there are three errors preventing it from running correctly.
Fix these then copy-paste the final result into Blackboard.

Use 0.25 m as your input for radius.

Lloyd Cawthorne - 22/03/19
"""

# SI units


CENTRIPETAL_ACCELERATION = 5.6
RADIUS = float(input("Radius in metres: "))
SPEED = (RADIUS*CENTRIPETAL_ACCELERATION)**0.5
print("The speed is", SPEED, "m/s.")
