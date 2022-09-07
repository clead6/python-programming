# -*- coding: utf-8 -*-
"""
PHYS20161 Week 8: Newton Raphson example

Simple example of implementing Newton Raphson to find root of x^2 - 2

Demonstrates convergence of solution.

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

# Main algorithm

# set up parameters
DIFFERENCE = 1
COUNTER = 0

DIFFERENCES = np.array([])
ROOTS = np.array([])

X_ROOT = X_START
ROOTS = np.append(ROOTS, X_ROOT)
# Repeatedly find x_n until the tolerance threshold is met.

while DIFFERENCE > TOLERANCE:

    COUNTER += 1

    X_TEST = X_ROOT
    X_ROOT = next_x(X_ROOT)

    DIFFERENCE = abs(X_TEST - X_ROOT)
    DIFFERENCES = np.append(DIFFERENCES, DIFFERENCE)
    ROOTS = np.append(ROOTS, X_ROOT)

# Solution plot
X_VALUES = np.linspace(0, 5, 100)

plt.xlabel('x')
plt.ylabel('f(x)')
plt.plot(X_VALUES, function(X_VALUES))
plt.plot(X_VALUES, 0 * X_VALUES, c='grey', dashes=[4, 4])
plt.scatter(ROOTS[0], function(ROOTS[0]), c='grey', label='x_0')
plt.scatter(ROOTS[1], function(ROOTS[1]), c='b', label='x_1')
plt.scatter(ROOTS[2], function(ROOTS[2]), c='g', label='x_2')
plt.scatter(X_ROOT, function(X_ROOT), c='k', label='x_root')

plt.plot(ROOTS[:2], np.full(2, function(ROOTS[0])), c='red',
         dashes=[4, 4], alpha=0.6)
plt.annotate("", xy=(ROOTS[1], function(ROOTS[1])),
             xytext=(ROOTS[1], function(ROOTS[0])),
             arrowprops=dict(arrowstyle="<->", color='red'))

plt.annotate("Difference", xy=(ROOTS[1],
                               (function(ROOTS[1]) + function(ROOTS[0])) / 2),
             xytext=(ROOTS[1]-0.9,
                     (function(ROOTS[1]) + function(ROOTS[0]) / 2)-2))

plt.plot(ROOTS[1:3], np.full(2, function(ROOTS[1])), c='red',
         dashes=[4, 4], alpha=0.6)
plt.annotate("", xy=(ROOTS[2], function(ROOTS[2])),
             xytext=(ROOTS[2], function(ROOTS[1])),
             arrowprops=dict(arrowstyle="<->", color='red'))

plt.annotate("Difference", xy=(ROOTS[2],
                               (function(ROOTS[2]) + function(ROOTS[1])) / 2),
             xytext=(ROOTS[2]-0.9,
                     (function(ROOTS[2]) + function(ROOTS[1]) / 2)-0.5))

plt.xlim(0, 5)
plt.ylim(-5, 20)
plt.legend()
plt.savefig('nr_differences.png', dpi=300)
plt.show()

print('2^0.5 = {:6.5f}'.format(X_ROOT))
print('This took {:d} iterations'.format(COUNTER))

# Convergence plot

ITERATIONS = np.arange(1, COUNTER + 1)

plt.title('Convergence of solution.')
plt.xlabel('Iteration')
plt.ylabel('Differences')
plt.plot(np.arange(COUNTER + 2), np.full(COUNTER + 2, TOLERANCE),
         c='grey', dashes=[4, 4], label='Tolerance')
plt.scatter(ITERATIONS, DIFFERENCES, c='k', label='Iterations')

plt.xlim(0, ITERATIONS[-1] + 1)
plt.ylim(-0.1, 2)
plt.legend()
plt.savefig('nr_convergence.png', dpi=300)
plt.show()
