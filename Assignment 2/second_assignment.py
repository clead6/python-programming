# -*- coding: utf-8 -*-
"""
________________TITLE________________
PHYS20161 - Assignment 2 - Doppler Spectroscopy
-------------------------------------
The following code analyses data recovered from a Doppler spectroscopy
analysis. It highlights a star's variation of velocity as a planet orbits
around it.
This program fits a function to the observed variation of the light emitted
from the star over the time and highlights the sinusoidal relation between
the velocity along line of sight and the time. It allows to find the period
and radius of orbit, as well as the velocity and mass of the planet.

Created 27/11/2020
Last Updated: 16/12/2020
@author: Clea Dronne, ID: 10475323
"""

import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as pc
from scipy.optimize import fmin
# from uncertainties import ufloat

SPEED_OF_LIGHT = pc.speed_of_light # in ms^-1
GRAVITATIONAL_CONSTANT = pc.gravitational_constant # in m^3 kg^-1 s^-2
ASTRONOMICAL_UNIT = pc.astronomical_unit # in m
JOVIAN_MASS = 1.89813E27 # in kg


def user_input():
    """ Asks the user for input on some constants.
    Returns:
        file_name1: string
        file_name2: string
        mass_star: float
        emitted_wavelength: float
    """
    general_input = input('The default files used in this program are '
                          'doppler_data_1.csv and doppler_data_2.csv. '
                          'The default values are 2.78 solar masses for the '
                          'mass of the star, 656.281 nm for the emitted '
                          'wavelength pi/2 for the line of sight angle. Do '
                          'you want to use different files/values? (Y/N) ')
    while general_input not in ('Y', 'N'):
        general_input = input('Answer not understood. Please use Y or N. ')
    if general_input == 'N':
        file_name1 = 'doppler_data_1.csv'
        file_name2 = 'doppler_data_2.csv'
        mass_star = 2.78 * 1.989E30 # in kg
        emitted_wavelength = 656.281 * 1E-9
        line_sight_angle = np.pi/2
    elif general_input == 'Y':
        file_name1 = input('Type the name of the first file. ')
        file_name2 = input('And the second file. ')
        mass_star = float(input('Input the mass of the star (in solar masses). '))
        mass_star *= 1.989E30
        emitted_wavelength = float(input('Input the emitted wavelength (in '
                                         'nm). '))
        emitted_wavelength *= 1E-9
        line_sight_angle = float(input('Input the line of sight angle (in '
                                       'radians). '))

    return (file_name1, file_name2, mass_star, emitted_wavelength,
            line_sight_angle)


def file_check(filename):
    """ Checks if file is in directory.
    Args:
        filename: string
    Returns:
        bool
    Raises:
        FileNotFoundError
    """
    try:
        file1 = open(filename, 'r')
        file1.close()
        return True
    except FileNotFoundError:
        print("'{0:s}' not found. Please check directory.".format(filename))
        return False


def read_data(file_name1, file_name2):
    """ Reads in date files and outputs data in 2D array.
    Args:
        file_name_1: string
        file_name_2: string
    Returns:
        file: [floats]
    """
    file1 = np.genfromtxt(file_name1, delimiter=',', skip_header=1)
    file2 = np.genfromtxt(file_name2, delimiter=',', skip_header=1)
    file = np.vstack((file1, file2))

    return file


def check_data(file):
    """ Reads in sorted data file and removes any incorrect data points.
    Args:
        file: string
    Returns:
        file: [floats]
    Raises:
        ValueError
        ZeroDivisionError
    """
    i = 0
    while i < len(file):
        try:
            float(file[i][0])
            float(file[i][1])
            float(file[i][2])

            if (np.isnan(file[i][0]) or np.isnan(file[i][1]) or
                    np.isnan(file[i][2])):
                raise ValueError
            if file[i][0] < 0 or file[i][1] <= 0 or file[i][2] <= 0:
                raise ZeroDivisionError
            i += 1
        except ValueError:
            file = np.delete(file, i, axis=0)
        except ZeroDivisionError:
            file = np.delete(file, i, axis=0)

    return file


def sort_data(file):
    """ Sorts the data file.
    Args:
        file
    Returns:
        sorted_file: [floats]
    """
    sorted_file = file[file[:, 0].argsort()]

    return sorted_file


def first_outlier_removal(sorted_file):
    """ Reads in the data file and removes very obvious outlier points.
    Args:
        sorted_file
    Returns:
        sorted_file: [floats]
    """
    mean = np.mean(sorted_file[:, 1])
    error = np.std(sorted_file[:, 1])
    minimum = mean - 5*error
    maximum = mean + 5*error
    i = 0
    while i < len(sorted_file):
        if minimum < sorted_file[i][1] < maximum:
            i += 1
        else:
            sorted_file = np.delete(sorted_file, i, axis=0)

    return sorted_file


def second_outlier_removal(sorted_file):
    """ Reads in the data file and removes other outlier points.
    Args:
        sorted_file
    Returns:
        sorted_file: [floats]
    """
    i = 2
    while i < len(sorted_file)-2:
        mean_values = np.mean(sorted_file[i-2:i+3, 1])
        mean_uncertainties = np.mean(sorted_file[i-2:i+3, 2])
        minimum = mean_values - 3*mean_uncertainties
        maximum = mean_values + 3*mean_uncertainties
        if minimum < sorted_file[i, 1] < maximum:
            i += 1
        else:
            sorted_file = np.delete(sorted_file, i, axis=0)

    return sorted_file


def observed_velocities(observed_wavelength, uncertainty_observed_wavelength,
                        emitted_wavelength, line_sight_angle,
                        speed_of_light=SPEED_OF_LIGHT):
    """ Calculates the observed velocities and their uncertainties from the
    values given for the observed wavelengths.
    Args:
        observed_wavelength
        uncertainty_observed_wavelength
        emitted_wavelength
        line_sight_angle
        speed_of_light
    Returns:
        observed_velocity
        uncertainty_observed_velocity
    """
    observed_velocity = (speed_of_light/np.sin(line_sight_angle))*((
        observed_wavelength/emitted_wavelength)-1)

    uncertainty_observed_velocity = ((speed_of_light *
                                      uncertainty_observed_wavelength)/
                                     emitted_wavelength)

    return observed_velocity, uncertainty_observed_velocity


def chi_squared(velocity_magnitude, angular_frequency, time, observed_velocity,
                uncertainty_observed_velocity, phase):
    """ Calculates the chi squared values for the velocity values.
    Args:
        velocity_magnitude
        angular_frequency
        time
        observed_velocity
        uncertainty_observed_velocity
        phase
    Returns:
        array of chi squared value
    """
    return np.sum(((velocity_magnitude*np.sin(angular_frequency*time+phase) -
                    observed_velocity) / uncertainty_observed_velocity)**2)


def minimisation_guesses_2d():
    """ Ask for user input on the guessed values used in the 2D minimisation.
    Returns:
        guess_velocity
        guess_frequency
        guess_phase
    """
    guess_input = input('The minimisation guesses are set to '
                        '50 ms^-1 for the velocity and 30E-8 rads^-1 for the '
                        'angular frequency. Do you want to use different '
                        'values? (Y/N) ')
    while guess_input not in ('Y', 'N'):
        guess_input = input('Answer not understood. Please use Y or N. ')
    if guess_input == 'Y':
        guess_velocity = float(input('Type the guess for velocity. '))
        guess_frequency = float(input('Now the guess for the angular frequency. '))

    elif guess_input == 'N':
        guess_velocity = 50
        guess_frequency = 3E-8

    return guess_velocity, guess_frequency


def minimisation_guesses_3d():
    """ Ask for user input on the guessed values used in the 3D minimisation.
    Returns:
        guess_velocity
        guess_frequency
        guess_phase
    """
    guess_input = input('The default values for the minimisation guesses are '
                        '50 ms^-1 for the velocity, 30E-8 rads^-1 for the '
                        'angular frequency and pi for the phase. Do you want '
                        'to use different values? (Y/N) ')
    while guess_input not in ('Y', 'N'):
        guess_input = input('Answer not understood. Please use Y or N. ')
    if guess_input == 'Y':
        guess_velocity = float(input('Type the guess for velocity. '))
        guess_frequency = float(input('Now the guess for the angular frequency. '))
        guess_phase = float(input('And the guess for the phase. '))

    elif guess_input == 'N':
        guess_velocity = 50
        guess_frequency = 3E-8
        guess_phase = np.pi

    return guess_velocity, guess_frequency, guess_phase


def minimisation_2d(time, observed_velocity, uncertainty_observed_velocity,
                    phase):
    """ Performs a minimisation for 2 arguments, the magnitude of the velocity
    and the angular frequency.
    Args:
        time
        observed_velocity
        uncertainty_observed_velocity
        phase
    Returns:
        velocity_magnitude
        angular_frequency
        minimum_chi_2
        reduced_chi_2
    """
    guess_velocity, guess_frequency = minimisation_guesses_2d()
    guess_f = (guess_velocity, guess_frequency)

    fitting = fmin(lambda x: chi_squared(x[0], x[1], time, observed_velocity,
                                         uncertainty_observed_velocity, phase),
                   guess_f, full_output=True)

    velocity_magnitude = fitting[0][0]
    angular_frequency = fitting[0][1]
    minimum_chi_2 = fitting[1]
    reduced_chi_2 = minimum_chi_2/(len(time)-2)

    return velocity_magnitude, angular_frequency, minimum_chi_2, reduced_chi_2


def minimisation_3d(time, observed_velocity, uncertainty_observed_velocity):
    """ Performs a minimisation for 3 arguments, the mangitude of the velocity,
    the angular frequency and the phase
    Args:
        time
        observed_velocity
        uncertainty_observed_velocity
    Returns:
        velocity_magnitude
        angular_frequency
        phase
        minimum_chi_2
        reduced_chi_2
    """
    guess_velocity, guess_frequency, guess_phase = minimisation_guesses_3d()
    guess_f = (guess_velocity, guess_frequency, guess_phase)

    fitting = fmin(lambda x: chi_squared(x[0], x[1], time, observed_velocity,
                                         uncertainty_observed_velocity, x[2]),
                   guess_f, full_output=True)

    velocity_magnitude = fitting[0][0]
    angular_frequency = fitting[0][1]
    phase = fitting[0][2]
    minimum_chi_2 = fitting[1]
    reduced_chi_2 = minimum_chi_2/(len(time)-3)

    return (velocity_magnitude, angular_frequency, phase, minimum_chi_2,
            reduced_chi_2)


def calculations(angular_frequency, velocity_magnitude, mass_star,
                 gravitational_constant=GRAVITATIONAL_CONSTANT,
                 astronomical_unit=ASTRONOMICAL_UNIT, jovian_mass=JOVIAN_MASS):
    """ Calculates the period, radius of orbit, velocity of the planet and
    mass of the planet.
    Args:
        velocity_magnitude
        angular_frequency
        mass_star
        gravitational_constant
        astronomical_unit
        jovian_mass
    Returns:
        period
        radius
        velocity_planet
        mass_planet
    """
    period = 2*np.pi/angular_frequency # in s
    radius = ((gravitational_constant*mass_star*period**2)/
              (4*np.pi**2))**(1/3) # in m
    velocity_planet = np.sqrt(gravitational_constant*mass_star/radius) # in m/s
    mass_planet = mass_star*velocity_magnitude/velocity_planet # in kg

    period /= (3600 * 24 *365) # in years
    radius /= astronomical_unit # in AU
    velocity_planet /= 1E3 # in km/s
    mass_planet /= jovian_mass # in jovian masses

    return period, radius, velocity_planet, mass_planet


def minimisation_input(time, observed_velocity, uncertainty_observed_velocity):
    """Asks the user whether they know the value for the phase. If they do, 2D
    minimisation is performed, otherwise 3D.
    Args:
        time
        observed_velocity
        uncertainty_observed_velocity
    Returns:
        velocity_magnitude
        angular_frequency
        minimum_chi_2
        reduced_chi_2
        phase
        uncertainty_phase
    """
    phase_input_1 = input('Do you know the value for the phase? If you know '
                          'it, a 2D minimisation will be performed, if not it '
                          'will be a 3D minimisation. (2 or 3) ')
    while phase_input_1 not in ('2', '3'):
        phase_input_1 = input('Answer not understood. Please use 2 or 3. ')

    if phase_input_1 == '2':
        phase_input_2 = input('The default value for phase is pi. Would you '
                              'like to use a different value? (Y/N) ')
        while phase_input_2 not in ('Y', 'N'):
            phase_input_2 = input('Answer not understood. Please use Y or N. ')
        if phase_input_2 == 'N':
            phase = np.pi
        elif phase_input_2 == 'Y':
            phase = float(input('Input the phase angle (in radians). '))
        (velocity_magnitude, angular_frequency, minimum_chi_2,
         reduced_chi_2) = minimisation_2d(time, observed_velocity,
                                          uncertainty_observed_velocity, phase)
        uncertainty_phase = 0

    elif phase_input_1 == '3':
        (velocity_magnitude, angular_frequency, phase, minimum_chi_2,
         reduced_chi_2) = minimisation_3d(time, observed_velocity,
                                          uncertainty_observed_velocity)

        uncertainty_phase = phase_uncertainties_calculations(
            velocity_magnitude, angular_frequency, time, observed_velocity,
            uncertainty_observed_velocity, phase)

    return (velocity_magnitude, angular_frequency, minimum_chi_2,
            reduced_chi_2, phase, uncertainty_phase)


def phase_uncertainties_calculations(velocity_magnitude, angular_frequency,
                                     time, observed_velocity,
                                     uncertainty_observed_velocity, phase):
    """ Calculates the uncertainty on the phase when 3D minimisation is
    performed.
    Args:
        velocity_magnitude
        angular_frequency
        time
        observed_velocity
        uncertainty_observed_velocity
        phase
    Returns:
        uncertainty_phase
    """
    step_phase = phase*1E-4
    varying_phase = phase

    minimum_chi_2 = chi_squared(velocity_magnitude, angular_frequency, time,
                                observed_velocity,
                                uncertainty_observed_velocity, phase)

    max_chi_2 = minimum_chi_2 + 1

    while minimum_chi_2 < max_chi_2:
        varying_phase += step_phase
        minimum_chi_2 = chi_squared(velocity_magnitude,
                                    angular_frequency, time,
                                    observed_velocity,
                                    uncertainty_observed_velocity,
                                    varying_phase)

    uncertainty_phase = (varying_phase - phase)

    return uncertainty_phase


def first_uncertainties_calculations(velocity_magnitude, angular_frequency,
                                     time, observed_velocity,
                                     uncertainty_observed_velocity, phase):
    """ Calculates uncertainties on the velocity magnitude and the
    angular frequency after the minimisation of the chi squared.
    Args:
        velocity_magnitude
        angular_frequency
        time
        observed_velocity
        uncertainty_observed_velocity
        phase
    Returns:
        uncertainty_velocity_magnitude
        uncertainty_angular_frequency
    """
    step_frequency = angular_frequency*1E-4
    varying_angular_frequency = angular_frequency
    step_velocity = velocity_magnitude*1E-4
    varying_velocity_magnitude = velocity_magnitude

    minimum_chi_2 = chi_squared(velocity_magnitude, angular_frequency, time,
                                observed_velocity,
                                uncertainty_observed_velocity, phase)
    max_chi_2 = minimum_chi_2 + 1

    while minimum_chi_2 < max_chi_2:
        varying_angular_frequency += step_frequency
        minimum_chi_2 = chi_squared(velocity_magnitude,
                                    varying_angular_frequency, time,
                                    observed_velocity,
                                    uncertainty_observed_velocity, phase)

    minimum_chi_2 = chi_squared(velocity_magnitude, angular_frequency, time,
                                observed_velocity,
                                uncertainty_observed_velocity, phase)

    while minimum_chi_2 < max_chi_2:
        varying_velocity_magnitude += step_velocity
        minimum_chi_2 = chi_squared(varying_velocity_magnitude,
                                    angular_frequency, time, observed_velocity,
                                    uncertainty_observed_velocity, phase)

    uncertainty_velocity_magnitude = (varying_velocity_magnitude -
                                      velocity_magnitude)
    uncertainty_angular_frequency = (varying_angular_frequency -
                                     angular_frequency)

    return uncertainty_velocity_magnitude, uncertainty_angular_frequency


def second_uncertainties_calculations(velocity_magnitude,
                                      uncertainty_velocity_magnitude,
                                      angular_frequency,
                                      uncertainty_angular_frequency,
                                      mass_star):
    """ Calculates uncertainties on the other variables from the
    calculations function.
    Args:
        velocity_magnitude
        uncertainty_velocity_magnitude
        angular_frequency
        uncertainty_angular_frequency
        mass_star
    Returns:
        velocity_magnitude: ufloat
        angular_frequency: ufloat
        period: ufloat
        radius: ufloat
        velocity_planet: ufloat
        mass_planet: ufloat
    """
    period, radius, velocity_planet, mass_planet = calculations(
        angular_frequency, velocity_magnitude, mass_star)

    uncertainty_period = period*uncertainty_angular_frequency/angular_frequency
    uncertainty_radius = 2/3 *uncertainty_period/period * radius
    uncertainty_velocity_planet = (velocity_planet *
                                   uncertainty_radius)/(2*radius)
    uncertainty_mass_planet = mass_planet * np.sqrt((
        uncertainty_velocity_magnitude/velocity_magnitude)**2+(
            uncertainty_velocity_planet/velocity_planet)**2)

    return (velocity_magnitude, angular_frequency, period, radius,
            velocity_planet, mass_planet, uncertainty_period,
            uncertainty_radius, uncertainty_velocity_planet,
            uncertainty_mass_planet)


def mesh_arrays(x_array, y_array):
    """ Calculates mesh arrays from 2 arrays.
    Args:
        x_array
        y_array
    Returns:
        x_array_mesh
        y_array_mesh
    """
    x_array_mesh, y_array_mesh = np.meshgrid(x_array, y_array)

    return x_array_mesh, y_array_mesh


def function_plot(time, velocity_magnitude, angular_frequency,
                  observed_velocity, uncertainty_observed_velocity, phase):
    """ Plots the data points for the observed velocity, their error bars for
    their uncertainty and the velocity.
    Args:
        time
        velocity_magnitude
        angular_frequency
        observed_velocity
        uncertainty_observed_velocity
        phase
    Returns:
        plot
    """
    plot = plt.figure(1)
    axes = plot.add_subplot(111)
    axes.scatter(time, observed_velocity, uncertainty_observed_velocity)
    axes.plot(time, velocity_magnitude*np.sin(angular_frequency*time+phase))
    axes.errorbar(time, observed_velocity, uncertainty_observed_velocity,
                  fmt='o', color='blue')

    axes.set_title('Velocity along line of sight against time')
    axes.set_xlabel('Time (s)')
    axes.set_ylabel('Velocity along line of sight $v_s$ (m.s$^{-1}$)')

    plt.savefig('figure1_velocity_against_time.png', dpi=300)
    plt.show()

    return plot


def contour_plot(time, observed_velocity, uncertainty_observed_velocity,
                 velocity_magnitude, angular_frequency, minimum_chi_2, phase):
    """ Plots a contour plot with the velocity magnitude on an axis, the
    angular frequency on the other and the chi squared values as a function.
    Args:
        time
        velocity_magnitude
        angular_frequency
        observed_velocity
        uncertainty_observed_velocity
        minimum_chi_2
        phase
    Returns:
        contour
    """
    x_array = np.linspace(25, 35, len(time))
    y_array = np.linspace(2E-8, 3E-8, len(time))
    x_array_mesh, y_array_mesh = mesh_arrays(x_array, y_array)

    figure2 = plt.figure(2)
    axes = figure2.add_subplot(111)
    axes.set_title('Chi squared')
    axes.set_xlabel('Velocity Magnitude $v_0$ (m.s$^{-1}$)')
    axes.set_ylabel(r'Angular frequency $\omega$ (rad.s$^{-1}$)')


    function_values = np.empty((0, len(x_array)))
    for y_value in y_array:
        row = np.array([])
        for x_value in x_array:
            row = np.append(row, chi_squared(x_value, y_value, time,
                                             observed_velocity,
                                             uncertainty_observed_velocity,
                                             phase))

        function_values = np.vstack((function_values, row))

    contour = axes.contour(x_array_mesh, y_array_mesh, function_values, 15)

    axes.clabel(contour, inline=1, fontsize=10)
    axes.scatter(velocity_magnitude, angular_frequency, minimum_chi_2,
                 marker=".", c='purple')
    axes.annotate('{:.2f}'.format(minimum_chi_2), (velocity_magnitude,
                                                   angular_frequency))

    plt.savefig('figure2_chi_squared_contour_plot.png', dpi=300)
    plt.show()

    return contour


def main():
    """ Main code for program. Calls for user input, calculte the velocities
    from the data files and calculates the chi squared values. The function
    also outputs the plots and the final resuls.
    Returns
    -------
    None.
    """
    (file_name1, file_name2, mass_star, emitted_wavelength,
     line_sight_angle) = user_input()

    if file_check(file_name1) and file_check(file_name2):
        data = check_data(read_data(file_name1, file_name2))
        sorted_data = second_outlier_removal(first_outlier_removal(
            sort_data(data)))

        time = sorted_data[:, 0] * 3600 * 24 * 365 # in s
        observed_wavelength = sorted_data[:, 1] * 1E-9 # in m
        uncertainty_observed_wavelength = sorted_data[:, 2] * 1E-9 # in m

        observed_velocity, uncertainty_observed_velocity = observed_velocities(
            observed_wavelength, uncertainty_observed_wavelength,
            emitted_wavelength, line_sight_angle)


        (velocity_magnitude, angular_frequency, minimum_chi_2, reduced_chi_2,
         phase, uncertainty_phase) = minimisation_input(
             time, observed_velocity, uncertainty_observed_velocity)

        (uncertainty_velocity_magnitude,
         uncertainty_angular_frequency) = first_uncertainties_calculations(
             velocity_magnitude, angular_frequency, time, observed_velocity,
             uncertainty_observed_velocity, phase)

        function_plot(time, velocity_magnitude, angular_frequency,
                      observed_velocity, uncertainty_observed_velocity, phase)

        contour_plot(time, observed_velocity, uncertainty_observed_velocity,
                     velocity_magnitude, angular_frequency, minimum_chi_2,
                     phase)

        (velocity_magnitude, angular_frequency, period, radius,
         velocity_planet, mass_planet, uncertainty_period,
         uncertainty_radius, uncertainty_velocity_planet,
         uncertainty_mass_planet) = second_uncertainties_calculations(
             velocity_magnitude, uncertainty_velocity_magnitude,
             angular_frequency, uncertainty_angular_frequency, mass_star)


        magnitude = np.floor(np.log10(angular_frequency))
        print('The velocity magnitude is {0:.2f}+/-{1:.2f} ms^-1 and the '
              'angular frequency is {2:.3e}+/-{3:.3f}e{4:.0f} rads^-1. '.format(
                  velocity_magnitude, uncertainty_velocity_magnitude,
                  angular_frequency,
                  uncertainty_angular_frequency*10**(-magnitude), magnitude))
        print('The fit has a reduced chi squared value of {0:.3f}.'.format(
            reduced_chi_2))
        print('The orbit has a period {0:.3f}+/-{1:.3f} years and a radius '
              '{2:.3f}+/-{3:.3f} AU.'.format(period, uncertainty_period,
                                             radius, uncertainty_radius))
        print('The planet has a velocity {0:.2f}+/-{1:.2f} kms^-1 and a '
              'mass {2:.3f}+/-{3:.3f} Jovian masses.'.format(
                  velocity_planet, uncertainty_velocity_planet, mass_planet,
                  uncertainty_mass_planet))

        if uncertainty_phase != 0:
            print('The phase angle is {0:.2f}+/-{1:.2f}'.format(
                phase, uncertainty_phase))

main()
