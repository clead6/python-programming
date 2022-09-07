# -*- coding: utf-8 -*-
"""
PHYS20161 Week 8: Newton Raphson example

Simple example of implementing Newton Raphson to find root of x^2 - 2



"""

import numpy as np
import matplotlib.pyplot as plt

# Initial parameters

X_START = 4.
TOLERANCE = 0.001

# Function definitions


def function(x_variable):
    """Returns x^2 - 2
    x_variable (float)
    """
    return x_variable**2 - 2.


def derivative(x_variable):
    """Returns  2x, derivative of x^2 - 2
    x_variable (float)
    """
    return 2. * x_variable


def next_x(previous_x):
    """
    Returns next value for x according to algorithm

    previous_x (float)

    """

    return previous_x - function(previous_x) / derivative(previous_x)


# Main code

# Initial plot

X_VALUES = np.linspace(0, 5, 100)

plt.title('Find 2^0.5', fontsize=14)
plt.xlabel('x', fontsize=14)
plt.ylabel('y', fontsize=14)

# x axis
plt.plot(X_VALUES, 0 * X_VALUES, c='grey', dashes=[4, 4], linewidth=2)

# function
plt.plot(X_VALUES, function(X_VALUES), label='f(x)', linewidth=2)

# first tangent
plt.scatter(X_START, function(X_START), c='red', label='x_0', s=100)
plt.plot(X_VALUES, derivative(X_START)*(X_VALUES - X_START)
         + function(X_START), label='tangent', linewidth=2)

# line from first intercept to function
plt.plot((next_x(X_START), next_x(X_START)), (0, function(next_x(X_START))),
         c='r', linewidth=2)

# second tangent
plt.scatter(next_x(X_START), function(next_x(X_START)), c='grey', label='x_1',
            s=100)
X_1 = next_x(X_START)
plt.plot(X_VALUES, derivative(X_1)*(X_VALUES - X_1)
         + function(X_1), label='tangent', linewidth=2)


plt.xlim(0, 5)
plt.ylim(-5, 20)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)
plt.legend(fontsize=14)
plt.savefig('nr_nextpoint.png', dpi=300)
plt.show()


# Main algorithm

# set up parameters
DIFFERENCE = 1
COUNTER = 0

X_ROOT = X_START

# Repeatedly find x_n until the tolerance threshold is met.

while DIFFERENCE > TOLERANCE:

    COUNTER += 1

    X_TEST = X_ROOT
    X_ROOT = next_x(X_ROOT)

    DIFFERENCE = abs(X_TEST - X_ROOT)

# Final plot

plt.xlabel('x')
plt.ylabel('f(x)')
plt.plot(X_VALUES, function(X_VALUES))
plt.plot(X_VALUES, 0 * X_VALUES, c='grey', dashes=[4, 4])
plt.scatter(X_ROOT, function(X_ROOT), c='k', label='x_root')

plt.scatter(X_START, function(X_START), c='red', label='x_0')

plt.xlim(0, 5)
plt.ylim(-5, 20)
plt.legend()
plt.show()

print('2^0.5 = {:6.5f}'.format(X_ROOT))
print('This took {:d} iterations'.format(COUNTER))
