# -*- coding: utf-8 -*-
"""
PHYS20161 Week 8 quiz: find off set 1

This code reads in data and finds the offset according to the polynomial
defined.

It does this by minimising the variance between the data and the model given
some initial parameters.

Lloyd Cawthorne 01/11/19

"""

import numpy as np
import matplotlib.pyplot as plt

STEP = 0.1
TOLERANCE = 1
STARTING_OFFSET = 0


def polynomial(x_variable, offset):
    """
    Returns -x^5 + 4 x^3 + offset

    x (float)
    offset (float)
    """
    return -x_variable**5 + 4 * x_variable**3 + offset


def is_float(number):
    """Checks if input is valid

    Returns True if number is float.
    """

    try:
        float(number)
        return True

    except ValueError:
        return False


INPUT_FILE = open('polynomial_data_1.csv', 'r')

DATA = np.zeros((0, 2))

for line in INPUT_FILE:

    split_up = line.split(',')
    if is_float(split_up[0]) and is_float(split_up[1]):
        temp = np.array([float(split_up[0]), float(split_up[1])])
        DATA = np.vstack((DATA, temp))

print(DATA)

# Fitting procedure
# offset, difference, and comparison_0,1,2 are all varied when running so we
# will keep write them in snake_case to distinguish from constants.

offset = STARTING_OFFSET
difference = np.sum((DATA[:, 1] - polynomial(DATA[:, 0], offset))**2)

print(difference)

while difference > TOLERANCE:

    comparison_0 = np.sum((DATA[:, 1] 
                           - polynomial(DATA[:, 0], offset))**2)
    print(comparison_0)

    comparison_1 = np.sum((DATA[:, 1]
                           - polynomial(DATA[:, 0], offset - STEP))**2)
    
    print(comparison_1)

    comparison_2 = np.sum((DATA[:, 1]
                           - polynomial(DATA[:, 0], offset - STEP))**2)
    
    print(comparison_2)

    if comparison_0 < comparison_1:
        difference = comparison_1 - comparison_0
        offset += STEP

    elif comparison_0 < comparison_2:
        difference = comparison_2 - comparison_0
        offset += STEP
    else:
        print('Failed to reach desired precision.')
        break

print('The fitted offset is {:.1f}.'.format(offset))

# Plot results

plt.title('Fitted function against data')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.scatter(DATA[:, 0], DATA[:, 1])
plt.plot(DATA[:, 0], polynomial(DATA[:, 0], offset), c='black')
plt.show()
