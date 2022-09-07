# -*- coding: utf-8 -*-
"""
PHYS20161 Week 8 Blackboard Quiz: Read and compare data

This code reads in data, manipulates it, and compares it to a function.

Fix 5 bugs to get the code working. Once it is working you can answer the main
part of the question (worth 5 marks). To get the remaining 5 marks, you need to
write a function that finds the reduced chi squared for the various phases
given (treat the phases as a degree of freedom).

This question is not negatively marked.

In this code many variables are written as constants (upper case) in accordance
with PEP8. As you can see the majority are not constant and have their values
updated. Could you write these routines in terms of functions instead?

Lloyd Cawthorne 31/10/19

"""
import numpy as np
import matplotlib.pyplot as plt


def sin_function(angle, phase_variable):
    """
    computes sin(angle + phi) for angle in degrees and phi in radians.

    angle (float)
    phase_variable (float)
    """
    return np.sin(np.deg2rad(angle) + phase_variable)

def chi_squared(x_values, phase_variables, function_data, uncertainties):
    """ Returns chi squared after comparing function and data for a given
    coefficient

     coefficient_variable (float)
     x_values array of floats
     function_data array of floats
     errors array of floats
     """

    prediction = sin_function(x_values, phase_variables)

    return np.sum(((prediction - function_data) / uncertainties)**2)

PHASES = np.array([0, np.pi / 5, np.pi / 3, np.pi / 2, 3 * np.pi / 4])

DATA_OPEN = False

try:
    INPUT_FILE = open('sin_data.txt', 'r')
    DATA_OPEN = True

except FileNotFoundError:
    print('Unable to open file.')

if DATA_OPEN:

    DATA = np.zeros((0, 3))
    SKIPPED_FIRST_LINE = False
    for line in INPUT_FILE:
        if not SKIPPED_FIRST_LINE:
            SKIPPED_FIRST_LINE = True

        else:
            split_up = line.split()
            temp = np.array([])
            temp = np.append(temp, (float(split_up[0]), float(split_up[1]), float(split_up[2])))
            DATA = np.vstack((DATA, temp))

    INPUT_FILE.close()

    ANGLES = np.linspace(np.min(DATA[:, 0]), np.max(DATA[:, 0]), 100)

    plt.errorbar(DATA[:, 0], DATA[:, 1], yerr=DATA[:, 2], fmt='o',
                 label='data')
    for phase in PHASES:
        plt.plot(ANGLES, sin_function(ANGLES, phase),
                 label=r'\phi = {:4.3f} (rad)'.format(phase))
    plt.legend(bbox_to_anchor=(1.04, 1))
    plt.grid(True, color='grey', dashes=[4, 2])
    plt.xlabel(r'\theta (degrees)')
    plt.ylabel(r'sin(\theta +\phi)')
    plt.show()

length_data = len(DATA)

# chi squared calculations, calls function chi_squared()
for i in PHASES:
    values = chi_squared(DATA[:,0], i, DATA[:,1], DATA[:,2])
    reduced_values = values/(length_data-1)
    print(reduced_values)