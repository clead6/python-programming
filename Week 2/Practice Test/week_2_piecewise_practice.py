# -*- coding: utf-8 -*-
"""
PHYS20161 week2 - if-elif scope practice

This code calculates the value of a discontinuous function given user input.

y(x)=

3cos(x ) for -90 <= x < 0

-2x + 3 for  0 <= x < 2

exp(x-2) - 2 for 2 <= x < 5

0  otherwise

The alignment throughout the function needs to be fixed such that the scope is
correct.

Once you have fixed this, match the inputs and outputs listed on BlackBoard.

Note: This code will trigger a refactor warning in PyLint; can you fix it?

Lloyd Cawthorne 13/09/19

"""

# import mathematical functions
import numpy as np


def function(x_variable):
    """Computes function as outlined in header.
    x_variable (float)
    """
    if -90 <= x_variable < 5:
        if x_variable < 0:
            x_radians = x_variable * np.pi / 180.0
            first_function = 3.0 * np.cos(x_radians)
            return first_function
        elif x_variable < 2:
            second_function = -2.0 * x_variable + 3.0
            return second_function
        else:
            third_function = np.exp(x_variable - 2.0) - 2.0
            return third_function
    else:
        return 0.0


X_INPUT_STRING = input("Enter an argument for the function: ")

# cast to float
X_INPUT = float(X_INPUT_STRING)

Y_OUTPUT = function(X_INPUT)
print('y(', X_INPUT, ') = ', Y_OUTPUT)
