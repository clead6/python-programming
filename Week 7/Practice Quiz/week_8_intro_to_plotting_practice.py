# -*- coding: utf-8 -*-
"""
PHYS20161 Week 8 quiz Intro to matplotlib PRACTICE

This code is setup to produce a plot of Fourier Series of a sawtooth wave.
http://mathworld.wolfram.com/SawtoothWave.html
http://mathworld.wolfram.com/FourierSeriesSawtoothWave.html

Select the correct options on BlackBoard to produce the plot displayed.

Lloyd Cawthorne 29/10/19

"""

import matplotlib.pyplot as plt
import numpy as np


def sawtooth(x_variable, period_variable, amplitude=1):
    """
    Outputs a sawtooth that that starts at origin,
    with period and amplitude as given.

    x_variable (float)
    period_variable (float)
    amplitude(float) [default =1]
    """

    return (amplitude * (x_variable / period_variable
                         - np.floor(x_variable / period_variable)))


def sine_terms(x_variable, period_variable, index):
    """
    Returns sine terms for a given index for a fourier series of a
    sawtooth wave.

    x_variable (float)
    period_variable (float)
    index (int)
    """
    return ((1 / index)
            * np.sin(2 * index * np.pi * x_variable / (period_variable)))


def fourier_sawtooth(x_variable, period_variable, order, amplitude=1):
    """
    Outputs a fourier series representing a sawtooth wave upto a given order
    in the summation that that starts at origin, with period and amplitude as
    given.

    x_variable (float)
    period_variable (float)
    order (int)
    amplitude(float) [default = 1]
    """
    terms = 0

    if order > 0:
        # As plot routine iterates over x axis, need to be careful how we
        # iterate over sum of terms
        indices = np.arange(1, order + 1)
        for index in indices:
            terms = terms + sine_terms(x_variable, period_variable, index)

    # return amplitude * (0.5 - 1/np.pi * np.sum(terms))
        return amplitude * (0.5 - 1 / np.pi * terms)

    # If we return a constant value, need to ensure this is the same
    # dimension as array for plotting. Example of an edge case that needs
    # attention
    return np.full(len(x_variable), amplitude / 2)


# Code goes here
NUMBER_OF_TERMS = 6  # number of terms in fourier series
PERIOD = 2
X_VALUES = np.linspace(-3.5, 3.5, 1000)
plt.title('Sawtooth and Fourier approximation upto {:d} terms'
          .format(NUMBER_OF_TERMS), 
        fontname='Times New Roman', fontsize=16)
plt.xlabel('x')
plt.ylabel('y(x)')
plt.plot(X_VALUES, sawtooth(X_VALUES, PERIOD), label='sawtooth(x)', c='black')
plt.plot(X_VALUES, fourier_sawtooth(X_VALUES, PERIOD, NUMBER_OF_TERMS),
         label='Fourier approx.', color='purple')
plt.ylim(-0.25, 1.25)
plt.yticks(np.arange(-0.25, 1.5, 0.25))
plt.xlim(-3.5, 3.5)
plt.grid(True, color='grey', dashes=[4, 2])
plt.legend(loc='lower center', ncol=2)


plt.savefig('plot.png', dpi=300)

plt.show()
