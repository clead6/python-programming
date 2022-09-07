# -*- coding: utf-8 -*-
"""
PHYS20161 Week 7 Quiz: Newton Raphson PRACTICE

Example of implementing Newton Raphson to find root of
3exp(-x^2) - tanh(x/3) - 3/4
Correct the bugs, then find the answers requested on BlackBoard.

Lloyd Cawthrne 17/10/20

"""

import numpy as np
import matplotlib.pyplot as plt

# Initial parameters

X_START = 1
TOLERANCE = 0.000001
#  Function definitions


def function(x_variable):
    """Returns 3exp(-x^2) - tanh(x/3) - 3/4
    x (float)
    """
    return 3 * np.exp(-x_variable**2) - np.tanh(x_variable / 3) - 3/4


def derivative(x_variable):
    """Returns derivative of 3exp(-x^2) - tanh(x/3) - 3/4
    
    x_variable (float)
    """
    return (-3*(np.exp(-x_variable**2) * 2 * x_variable) 
            - (1-(np.tanh(x_variable / 3))**2) / 3)


def next_x_function(previous_x):
    """
    Returns next value for x according to algorithm

    previous_x (float)

    """

    return previous_x - function(previous_x) / derivative(previous_x)


def newton_raphson(x_start=X_START, tolerance=TOLERANCE,
                   next_x=next_x_function):
    """Iterates Newton Raphson algorithm until difference between succesive
    solutions is less than tolerance.
    Args:
        x_start: float, kwarg
        tolerance: float, kwarg
        next_x: function returning float, kwarg
    Returns:
        x_root: float
        counter: int
    """
    # set up parameters
    difference = 1
    counter = 0
    x_root = x_start

    # Repeatedly find x_n until the tolerance threshold is met.
    while difference > tolerance:

        counter += 1

        x_test = x_root
        x_root = next_x(x_root)

        difference = np.abs(x_test - x_root)

    return x_root, counter


# Main code

X_VALUES = np.linspace(-6, 2, 10)

X_ROOT, COUNTER = newton_raphson()

# Final plot

plt.xlabel('x')
plt.ylabel('f(x)')
plt.plot(X_VALUES, function(X_VALUES))
plt.plot(X_VALUES, 0 * X_VALUES, c='grey', dashes=[4,4])
plt.scatter(X_ROOT, function(X_ROOT), c='k', label='x_root')

plt.scatter(X_START, function(X_START), c='red', label='x_0')

plt.xlim(-6, 2)
plt.ylim(-1, 2.5)
plt.legend()
plt.show()

print('Root = {:.5f}'.format(X_ROOT))
print('This took {:d} iterations'.format(COUNTER))