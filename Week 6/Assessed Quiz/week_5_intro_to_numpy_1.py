# -*- coding: utf-8 -*-
"""
PHYS20161 Week 5 quiz: Intro to Numpy

Lloyd Cawthorne 14/06/19

You are given an array 'argument_array' with entries x_i.
The for loop is set up to print a function with these entries f(x_i).

Use the correct function to return the results requested on BB. Then select the
function from the drop-down menu.

"""

import numpy as np

ARGUMENT_ARRAY = np.array([1.0, 1.1, 2.0, 2.6, 3.2, 4.0, 5.8, 6.4, 7.4, 7.9,
                           8.1, 9.2, 9.5, 9.8, 10.2])

FUNCTION_ARRAY = np.rad2deg(ARGUMENT_ARRAY)

for index in FUNCTION_ARRAY:
    print('{:3.2f}'.format(index))
