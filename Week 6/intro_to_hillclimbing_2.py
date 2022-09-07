# -*- coding: utf-8 -*-
"""
PHYS20161 Week 8 Example maximum of parabola.

Demonstrates and visualises hill-climbing approach for finding maximum of
a parabola.

"""

import numpy as np
import matplotlib.pyplot as plt

# Fitting parameters

X_START = -1.5
STEP = 0.01
TOLERANCE = 0.001

# Functions


def parabola(x_variable):
    """Returns -2x^4 - 4x^2 + 5x - 10
    x_variable (float)
    """
    return -2 * x_variable**4 - 4. * x_variable**2 + 5. * x_variable + 10.


def plot_parabola(x_values, parabola_function):

    """Returns plot object for parabola and x values given
    x_values np.array(float)
    parabola function that returns float
    """

    plot, = plt.plot(x_values, parabola_function(x_values))
    plt.xlabel('x values')
    plt.ylabel('f(x)')

    return plot


# Main code

X_VALUES = np.linspace(-2., 2., 100)

# Set initial parameters
X_MAXIMUM = X_START
PARABOLA_MAXIMUM = parabola(X_START)

# Display plot with startig point
plt.scatter(X_MAXIMUM, PARABOLA_MAXIMUM, label='Starting_point', color='k')

# Set counter and difference
COUNTER = 0
DIFFERENCE = 1

# Hillclimbing algorithm
while DIFFERENCE > TOLERANCE:

    COUNTER += 1

    # Look either side of point
    PARABOLA_TEST_PLUS = parabola(X_MAXIMUM + STEP)
    PARABOLA_TEST_MINUS = parabola(X_MAXIMUM - STEP)

    # Set new values if a better point is found
    if PARABOLA_TEST_PLUS > PARABOLA_MAXIMUM:

        DIFFERENCE = PARABOLA_TEST_PLUS - PARABOLA_MAXIMUM
        PARABOLA_MAXIMUM = PARABOLA_TEST_PLUS
        X_MAXIMUM += STEP

    elif PARABOLA_TEST_MINUS > PARABOLA_MAXIMUM:

        DIFFERENCE = PARABOLA_TEST_MINUS - PARABOLA_MAXIMUM
        PARABOLA_MAXIMUM = PARABOLA_TEST_MINUS
        X_MAXIMUM -= STEP

# Plot result
plot_parabola(X_VALUES, parabola)
plt.scatter(X_MAXIMUM, PARABOLA_MAXIMUM, label='Maximum', color='r')
plt.legend()
plt.show()

print('f({0:4.3f}) = {1:5.3f} is the maximum point'.
      format(X_MAXIMUM, PARABOLA_MAXIMUM))
print('This took {0:d} iterations.'.format(COUNTER))
