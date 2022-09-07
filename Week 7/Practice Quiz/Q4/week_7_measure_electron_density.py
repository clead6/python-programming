# -*- coding: utf-8 -*-
"""
PHYS20161 Week 7 Quiz Practice: Measure conduction electron density of metals

An experiment is setup to measure the resultant Hall voltage from applying
a magnetic field perpendicular to a current across various samples of a metal.
https://en.wikipedia.org/wiki/Hall_effect

This voltage is directly proportional to the number of electrons in the
conduction band of the sample. From this, we can determine the number of
conduction electrons each atom contributes to the band.

This code reads in data and then performs a minimised chi squared fit to
determine the charge carrier density.

Lloyd Cawthorne 27/07/20
"""

import numpy as np
import matplotlib.pyplot as plt

# Constants

TOLERANCE = 0.001
STARTING_VALUE = 0.1
STARTING_STEP = 0.05
MAX_ITERATIONS = 100

FILENAME = 'silver_data.csv'

ELECTRON_CHARGE = 1.602 * 10**-19

METAL = 'silver'
SYMBOL = 'Ag'

ATOMIC_WEIGHT = 107.868 #  Silver
DENSITY = 10.49 #  g/cm^3 Silver

AVOGADRO_NUMBER = 6.022 * 10**23

MOLES_PER_CM_CUBED = 1. / (AVOGADRO_NUMBER * 100**3)

# Function definitions

def is_float(entry):
    """Checks if entry is float,
    returns bool"""
    try:
        float(entry)
        return True
    except ValueError:
        return False


def file_check(filename):
    """Checks if file is in directory.
    Args:
        filename: string
    Returns:
        bool
    Raises:
        FileNotFoundError
    """
    try:
        open(filename)
        filename.close()
        return True
    except FileNotFoundError:
        return False


def read_data(filename):
    """Reads in date file, skipping non-numeric values, and outputs data in
    arrays.
    Args:
        filename: string
    Returns:
        distances [floats]
        distances_uncertainties [floats]
        times [floats]
        times_uncertainties [floats]
        mass_dropped  [floats]
        mass_trolley [floats]
    """

    b_fields = np.array([])
    voltages = np.array([])
    voltage_uncertainty = np.array([])
    currents = np.array([])
    thicknesses = np.array([])
    with open(filename, 'r') as file:
        for line in file:
            if line[0] != '%':
                line_split = line.split(',')
                if all(is_float(entry) for entry in line_split):
                    b_fields = np.append(b_fields, float(line_split[0]))
                    voltages = np.append(voltages, float(line_split[1]))
                    voltage_uncertainty = np.append(voltage_uncertainty
                                                    , float(line_split[2]))
                    currents = np.append(currents, float(line_split[3]))
                    thicknesses = np.append(thicknesses,
                                            float(line_split[4]))

    return (b_fields, voltages, voltage_uncertainty, currents, thicknesses)

def array_sections(array):
    """Given array of sections of repeated values, finds the indices where the
    values change
    Args:
        array: numpy array
    Returns:
        indices: numpy arrays of ints
    """
    indices = np.where(array[:-1] != array[1:])[0]
    indices = indices + 1
    indices = np.insert(indices, 0, 0)
    indices = np.append(indices, len(array) - 1)
    return indices

def electrons_per_atom(electron_density):
    """
    Given the electron density in m^-3, determines the number of electrons per
    atom.

    Parameters
    ----------
    electron_density : float

    Returns
    -------
    float
    """
    atoms_per_cm3 = DENSITY * AVOGADRO_NUMBER / ATOMIC_WEIGHT
    electron_density_cm3 = electron_density / 100**3

    return electron_density_cm3 / atoms_per_cm3


def voltage(current, b_field, electron_density, thickness):
    """
    Returns the Hall voltage.

    Parameters
    ----------
    current : float
        Amps
    b_field : float
        Tesla
    electron_density : float
        electrons/m^3
    thickness : float
        m
    Returns
    -------
    float
        Hall voltage, V

    """
    return(current * b_field / (electron_density * ELECTRON_CHARGE
                                * (thickness / 100)))


def chi_squared(prediction, data, uncertainty):
    """Returns chi squared
    Args:
        prediction: numpy array of floats
        data: numpy array of floats
        uncertainty: numpy array of floats
    Returns:
        chi squared (float)
    """

    return np.sum(((prediction - data) / uncertainty)**2)


def hillclimbing_minimisation(function, starting_value):
    """Runs a hill climbing algorithm to find the minimum of a function.
    Has a dynamic step size to improve efficiency and has a timeout break.
    Args:
        function, function that takes one variable and returns a float
        statting_value: float
    Returns:
        minimum_value: float
        function_minimum: foat
        counter: int
    """
    counter = 0
    difference = 1
    step_size = STARTING_STEP
    function_minimum = function(starting_value)
    minimum_value = starting_value

    while difference > TOLERANCE:
        counter += 1
        function_plus = function(minimum_value + step_size)
        function_minus = function(minimum_value - step_size)

        if function_plus < function_minimum:
            difference = np.abs(function_minimum - function_plus)
            function_minimum = function_plus
            minimum_value += step_size

        elif function_minus < function_minimum:
            difference = np.abs(function_minimum - function_minus)
            function_minimum = function_minus
            minimum_value -= step_size
        else:
            step_size /= 10
        if counter == MAX_ITERATIONS:
            print('Failed to find solution after {0:d} iterations.'.
                  format(counter))
            break
    return minimum_value, function_minimum, counter


def transpose_formatting(base, target, decimals=3):
    """
    Returns the appropriate mantissa to have formatting between two numbers
    to the same power of 10.

    Parameters
    ----------
    base : float
        Number that sets the format.
    target : float
        Number that needs to be consistent.
    decimals : float, optional
        Number of decimals to return. The default is 3.

    Returns
    -------
    mantissa : foat
    """
    power_of_ten = np.floor(np.log10(base))

    mantissa = np.round(target / 10**power_of_ten, decimals=decimals)

    return mantissa


def plot_result(bfields_data, voltage_data,
                currents, thicknesses, electron_density_calculated):
    """Generates a plot of the found result. Iterates the plot by different
    trolley masses. Maximum 6 lines, restriction due to colour list.
    Args:
        heights_data: numpy array of floats
        massed_dropped: numpy array of floats
        masses_trolley: numpy array of floats
        velocity_data: numpy array of floats
        g_calulated: [g_found, g_uncertainty]
    Returns:
        None
    """
    electron_density_found = electron_density_calculated[0]
    sigma = electron_density_calculated[1]


    colours = ['b', 'r', 'g', 'k', 'm', 'c']
    data_split = array_sections(currents)

    for index, entry in enumerate(data_split):
        if index >= len(data_split) - 1:
            # index used to locate next entry; last entry returns an IndexError
            break

        plt.plot(bfields_data[entry:data_split[index + 1]],
                 voltage(currents[entry:data_split[index + 1]],
                         bfields_data[entry:data_split[index + 1]],
                         electron_density_found,
                         thicknesses[entry:data_split[index + 1]]),
                 color=colours[index],
                 label='I = {0:g} A, d = {1:.2f} cm'.
                 format(currents[entry],
                        thicknesses[entry] * 100))
        plt.errorbar(bfields_data[entry:data_split[index + 1]],
                     voltage_data[0][entry:data_split[index + 1]],
                     yerr=voltage_data[1][entry:data_split[index + 1]],
                     fmt='o', color=colours[index])
    plt.title('{0:s} electron density = {1:.3g}+/- {2:.2f}e+{3:d}'
              ' electrons/m^3.'.format(
                  SYMBOL, electron_density_found,
                  transpose_formatting(electron_density_found, sigma),
                  np.int(np.floor(np.log10(electron_density_found)))))
    plt.xlabel('B field (T)')
    plt.ylabel('Voltage (V)')
    plt.legend(bbox_to_anchor=(1.05, 1))
    plt.show()

    return 0

def main():
    """Main code for programme. Reads data then performs a minimised chi
    squared fit with 1 sigma estimations. Plots result"""
    (b_fields, voltages, voltage_uncertainties, currents,
     thicknesses) = read_data(FILENAME)
    # Convert to V from mV and m from cm
    voltages /= 1000
    voltage_uncertainties /= 1000
    #thicknesses /= 100
    
    #array slicing
    index = array_sections(thicknesses)[1]
    b_fields = b_fields[:index]
    voltages = voltages[:index]
    voltage_uncertainties = voltage_uncertainties[:index]
    currents = currents[:index]
    thicknesses = thicknesses[:index]

    # Minimised chi squared fit
    # As the densities are very large (~e28), we instead consider moles per
    # cm cubed as it is easier to work with numbers close to, or below, unity.
    (electron_density_found, minimum_chi_squared,
     counter) = hillclimbing_minimisation(
         lambda x: chi_squared(voltage(currents, b_fields, x * (AVOGADRO_NUMBER * 100**3), thicknesses), voltages, voltage_uncertainties)
         , STARTING_VALUE)
    print("done")

    # Need to round as well as cast. np.int floors the value.
    conduction_electrons_per_atom = np.int(np.round(electrons_per_atom(
        electron_density_found / MOLES_PER_CM_CUBED)))
    # Write 1 standard deviation estimation here, ideally it should be a
    # function. Best way is to find +/- 1 sigma span, then divide by 2.
    print(minimum_chi_squared)    
    (electron_density_plus_sigma, chi_squared_function, counter2) = hillclimbing_minimisation(lambda x: abs(chi_squared(voltage(currents, b_fields, x * (AVOGADRO_NUMBER * 100**3), thicknesses), voltages, voltage_uncertainties) - minimum_chi_squared - 1)
         , STARTING_VALUE)
    sigma = abs(electron_density_plus_sigma-electron_density_found)
    
    plot_result(b_fields, [voltages, voltage_uncertainties], currents,
                thicknesses, [electron_density_found / MOLES_PER_CM_CUBED
                              , 0.00])
    print('Reduced chi squared: {0:.4f}.'.format(minimum_chi_squared
                                                 / (len(voltages) - 1)))
    print('Iterations: {0:d}.'.format(counter))
    print('Minimum Chi Squared: {0:.4g}.'.format(minimum_chi_squared))
    print('Electron density = {0:.3g} +/- {1:.3g} electrons/m^3.'.
          format(electron_density_found / MOLES_PER_CM_CUBED,
                 sigma / MOLES_PER_CM_CUBED))
    print('{0:s} has {1:d} conduction electron(s) per atom.'.
          format(METAL.capitalize(), conduction_electrons_per_atom))

    return 0

main()
