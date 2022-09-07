# -*- coding: utf-8 -*-
"""
PHYS20161 Week 7 Quiz: Measuring halflife of Cm 251

An experiment is set up to measure the halflife of Curium 251 by observing the
decrease in activity. Different samples were used along with different
detectors at different distances. Due the variance in distance, each detector
reads a different decay rate, though these can all be reconsiled with
appropriate solid ange.

This code reads in data to extract t_1/2 by considering nuclear decay. It does
this by performing a minimised chi squared fit using hillclimbing algorithm.

Lloyd Cawthorne 31/07/20
"""

import numpy as np
import matplotlib.pyplot as plt

# Constants

STARTING_VALUE = 0.0007
STARTING_STEP = 0.0001
TOLERANCE = 0.001
MAX_ITERATIONS = 100
FILENAME = 'cm_251_data_2.csv'

DETECTOR_AREA = np.pi * 0.05**2
ATOMIC_WEIGHT = 251.082

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
        file = open(filename,'r')
        file.close()
        return True
    except FileNotFoundError:
        print("'{0:s}' not found. Please check directory.".format(filename))
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

    time = np.array([])
    counts = np.array([])
    count_uncertainties = np.array([])
    count_times = np.array([])
    count_times_uncertainties = np.array([])
    masses = np.array([])
    detector_distance = np.array([])
    with open(filename, 'r') as file:
        for line in file:
            if line[0] != '%':
                line_split = line.split(',')
                if all(is_float(entry) for entry in line_split):
                    if float(line_split[2])!=0.0 or float(line_split[3])!= 0.0 or float(line_split[4])!= 0.0:
                        time = np.append(time, float(line_split[0]))
                        counts = np.append(counts, float(line_split[1]))
                        count_uncertainties = np.append(count_uncertainties, float(line_split[2]))
                        count_times = np.append(count_times, float(line_split[3]))
                        count_times_uncertainties = np.append(count_times_uncertainties, float(line_split[4]))
                        masses = np.append(masses, float(line_split[5]))
                        detector_distance = np.append(detector_distance, float(line_split[6]))
    
    return (time, counts, count_uncertainties, count_times,
            count_times_uncertainties, masses, detector_distance)

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

def number_of_nuclei(mass):
    """Given a mass, returns the number of nuclei.
    Args:
        mass: float
    Returns:
        nuclei: float
    """

    avogadro_number = 6.022 * 10**23

    moles = mass / ATOMIC_WEIGHT

    return moles * avogadro_number


def solid_angle(distance):
    """
    Returns the solid angle assuming the area of the detector is far smaller
    than the sphere at distance given.

    Parameters
    ----------
    distance : float

    Returns
    -------
    float
    """

    return DETECTOR_AREA / (4 * np.pi * distance**2)


def activity(time, decay_constant, starting_nucleons):
    """
    Returns the total activity of a sample given the decay constant and how
    much time has passed since the initial number of nucleons were known.

    Parameters
    ----------
    time : float
        seconds.
    decay_constant : float
        1 / seconds.
    starting_nucleons : int

    Returns
    -------
    activity: float
        becquerels.
    """

    return decay_constant * starting_nucleons * np.exp(- decay_constant * time)


def halflife(decay_constant):
    """
    Returns the halflife in miniutes given the decay constant.

    Parameters
    ----------
    decay_constant : float
        decays per second.

    Returns
    -------
    halflife : float
        minutes
    """
    return np.log(2) / (decay_constant * 60)


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


def uncertainty_propagation(function, numerator, denominator,
                            numerator_uncertainty, denominator_uncertainty):
    """Propogates uncertainties for function = numerator / denominator"""

    return (np.abs(function) * np.sqrt((numerator_uncertainty / numerator)**2
                                       + (denominator_uncertainty
                                          / denominator)**2))


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


def plot_result(times_data, masses, detector_distance,
                activity_data, lambda_calculated):
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
    lambda_found = lambda_calculated
    sigma = 0.000
    halflife_sigma = uncertainty_propagation(halflife(lambda_found),
                                             lambda_found, 1, sigma, 0)
    colours = ['b', 'r', 'g', 'k', 'm', 'c']
    data_split = array_sections(detector_distance)

    for index, entry in enumerate(data_split):
        if index >= len(data_split) - 1:
            # index used to locate next entry; last entry returns an IndexError
            break
        
        plt.plot(times_data[entry:data_split[index + 1]],
                  activity(times_data[entry:data_split[index + 1]],
                          lambda_found,
                          number_of_nuclei(masses[entry:data_split[index + 1]])
                          * solid_angle(detector_distance[entry:data_split[index + 1]])),
                  color=colours[index],
                  label='m = {0:g} g, d = {1:.2f} cm'.
                  format(masses[entry],
                        detector_distance[entry]))

        plt.errorbar(times_data[entry:data_split[index + 1]],
                      activity_data[0][entry:data_split[index + 1]],
                      yerr=activity_data[1][entry:data_split[index + 1]],
                      fmt='o', color=colours[index])
    plt.yscale('log', nonposy='clip')
    plt.title('t_1/2 = {0:.2f} +/- {1:.2f} min'.format(halflife(
        lambda_found), halflife_sigma))
    plt.xlabel('Time (s)')
    plt.ylabel('Observed activity (Bq)')
    plt.legend(bbox_to_anchor=(1.05, 1))
    plt.show()

    return 0

def main():
    """Main code for programme. Reads data then performs a minimised chi
    squared fit with 1 sigma estimations. Plots result"""
    if file_check(FILENAME):

        (time, counts, count_uncertainties, count_times,
         count_times_uncertainties, masses,
         detector_distance) = read_data(FILENAME)
        # Convert to s from min and to m from cm
        time *= 60
        detector_distance /= 100
        
        # array slicing
        # index = array_sections(masses)[1]
        # print(index)
        
        # time = time[:index]
        # counts = counts[:index]
        # count_times = count_times[:index]
        # count_uncertainties = count_uncertainties[:index]
        # count_times_uncertainties = count_times_uncertainties[:index]
        # masses = masses[:index]
        # detector_distance = detector_distance[:index]
        
        activity_data = np.array([])
        activity_data = np.vstack((counts / count_times,uncertainty_propagation(counts / count_times,
                                                 counts,
                                                 count_times,
                                                 count_uncertainties,
                                                 count_times_uncertainties)))        

        # Minimised chi squared fit
        lambda_found, minimum_chi_squared, counter = hillclimbing_minimisation(
            lambda x: chi_squared((activity(time, x,
                                            number_of_nuclei(masses))
                                   * solid_angle(detector_distance)),
                                  activity_data[0], activity_data[1])
            , STARTING_VALUE)
        
        # Write 1 standard deviation estimation here, ideally it should be a
        # function. Best way is to find +/- 1 sigma span, then divide by 2.
  
        (lambda_plus_sigma, chi_squared_function, counter2) = hillclimbing_minimisation(
            lambda x: abs(chi_squared((activity(time, x,
                                            number_of_nuclei(masses))
                                   * solid_angle(detector_distance)),
                                  activity_data[0], activity_data[1]) - minimum_chi_squared - 1)
            , STARTING_VALUE)
        
        std = abs(lambda_plus_sigma-lambda_found)

        plot_result(time, masses, detector_distance, activity_data,
                    lambda_found)
        print('Reduced chi squared: {0:.2f}.'.format(minimum_chi_squared
                                                     / (len(time) - 1)))
        print('Iterations: {0:d}.'.format(counter))
        print('Minimum Chi Squared: {0:.2f}.'.format(minimum_chi_squared))
        print('t_1/2 = {0:.2f} +/- {1:.2f} min.'.
              format(halflife(lambda_found),
                     uncertainty_propagation(halflife(lambda_found),
                                             lambda_found, 1, std, 0)))

    return 0

main()
