# -*- coding: utf-8 -*-
"""
PHYS20161 Blackboard Quiz week 8 Read and compare data function PRACTICE

This code reads in data, manipulates it, and compares it to a function.

Fix 5 bugs to get the code working. Once it is working you can answer the main
part of the question (worth 5 marks). To get the remaining 5 marks, you need to
write a function that finds the reduced chi squared for the various phases
given (treat the phases as a degree of freedom).

This question is not negatively marked.

Lloyd Cawthorne 1/11/19

"""
import numpy as np
import matplotlib.pyplot as plt

PHASES = np.array([0, np.pi / 6, np.pi / 3, np.pi / 2, np.pi])


def function(angle_variable, phase_variable):
    """
    computes 3 cos(angle + phi)^2 sin(angle+phi) for angle in degrees and phi
    in radians  (float).

    angle_variable (float)
    phase_variable (float)
    """
    return (3 * np.cos(np.deg2rad(angle_variable) + phase_variable)**2
            * np.sin(np.deg2rad(angle_variable) + phase_variable))

def chi_squared(x_values, phase_variables, function_data, uncertainties):
    """ Returns chi squared after comparing function and data for a given
    coefficient

     coefficient_variable (float)
     x_values array of floats
     function_data array of floats
     errors array of floats
     """

    prediction = function(x_values, phase_variables)

    return np.sum(((prediction - function_data) / uncertainties)**2)

DATA_OPEN = False

try:
    INPUT_FILE = open('week_8_function_data_practice.txt', 'r')
    DATA_OPEN = True

except FileNotFoundError:
    print('Unable to open file.')

if DATA_OPEN:

    data = np.zeros((0, 3))
    skipped_first_line = False
    for line in INPUT_FILE:

        if not skipped_first_line:
            skipped_first_line = True

        else:

            split_up = line.split()
            
            temp = np.array([])
            temp = np.append(temp, (float(split_up[0]), float(split_up[1]), float(split_up[2])))
            
            data = np.vstack((data, temp))
            

    INPUT_FILE.close()

    angles = np.linspace(np.min(data[:, 0]), np.max(data[:, 0]), 100)

    plt.errorbar(data[:, 0], data[:, 1], yerr=data[:, 2], fmt='o',
                 label='data')
    for phase in PHASES:
        plt.plot(angles, function(angles, phase),
                 label=r'\phi = {:4.3f} (rad)'.format(phase))
    plt.legend(bbox_to_anchor=(1.04, 1))
    plt.grid(True, color='grey', dashes=[4, 2])
    plt.xlabel(r'\theta (degrees)')
    plt.ylabel(r'cos(\theta +\phi)')
    plt.show()

length_data = len(data)

# chi squared calculations, calls function chi_squared()
for i in PHASES:
    values = chi_squared(data[:,0], i, data[:,1], data[:,2])
    reduced_values = values/(length_data-1)
    print(reduced_values)
    