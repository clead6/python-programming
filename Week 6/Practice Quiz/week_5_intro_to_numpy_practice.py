# -*- coding: utf-8 -*-
"""
PHYS20161 Week 5 PRACTICE intro to numpy

Using the array provided, apply various numpy functions as listed on BB and
match them to the appropriate outputs.

Lloyd Cawthorne 18/10/19

"""
import numpy as np

ARGUMENT_ARRAY = np.array([0.6, 1.5, 2.4, 4.0, 4.9, 5.4,
                           6.56, 7.7, 8.4, 9.2, 10.0])

FUNCTION_ARRAY = np.deg2rad(ARGUMENT_ARRAY)

for element in FUNCTION_ARRAY:
    print('{:3.2f}'.format(element))
