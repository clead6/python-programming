# -*- coding: utf-8 -*-
"""
________________TITLE________________
PHYS20161 - Assignment 1 - Bouncy Ball
-------------------------------------
The following code:
    1. Asks user for input on the height at which the ball is dropped, until
    which height it should bounce and the efficiency coefficient determining
    the number of bounces.
    2. Checks the inputed values follow initial conditions and prompts
    the user for new input if they are not respected.
    3. Calculates the number of bounces of the ball and the time taken for
    these bounces.

Created 12/10/2020
Last Updated: 30/10/2020
@author: Clea Dronne, ID: 10475323
"""

import numpy as np

GRAVITATIONAL_CONSTANT = 9.80665


def user_input():
    """
    Asks the user for input and checks it for ValueError.

    No Parameters

    Returns: efficiency_checks()
    """
    while True:
        try:
            efficiency_input = float(input('What is the efficiency? '))
            start_height_input = float(input('What is the initial height? '))
            minimum_height_input = float(input('What is the reached height? '))

            return efficiency_checks(efficiency_input, start_height_input,
                                     minimum_height_input)

        except ValueError:
            print('\nInput is not valid.')


def efficiency_checks(efficiency, start_height, minimum_height):
    """
    Checks the inputed value for efficiency.

    Parameters
    ----------
    efficiency : float, coefficient giving the energy lost at each bounce.
    start_height : float, height at which the ball is dropped.
    minimum_height : float, height above which the number of bounces is
    calculated.

    Returns: height_checks()
    """
    while not 0 < efficiency < 1:
        if efficiency == 0:
            print('\nThe ball will not bounce. Please input a new '
                  'efficiency.')
        elif efficiency == 1:
            print('\nThe ball will bounce infinitely. Please input a new '
                  'efficiency.')
        else:
            print('\nYour efficiency input is not valid. Please input a new '
                  'efficiency.')
        efficiency = float(input('What is the efficiency? '))

    return height_checks(efficiency, start_height, minimum_height)


def height_checks(efficiency, start_height, minimum_height):
    """
    Checks the inputed value for both the start height and the minimum height.

    Parameters
    ----------
    efficiency : float, coefficient giving the energy lost at each bounce.
    start_height : float, height at which the ball is dropped.
    minimum_height : float, height above which the number of bounces is
    calculated.

    Returns:
    finite_sum() if minimum_height != 0
    infinite_sum() if minimum_height = 0
    """

    while start_height < 0 or minimum_height < 0:
        print('\nYou have inputted negative values for heights. Please input '
              'new heights.')
        start_height = float(input('What is the initial height? '))
        minimum_height = float(input('What is the reached height? '))

    while start_height < minimum_height:
        print('\nYou have inputted a drop height smaller than the minimum '
              'height, the ball will not be dropped. Please input new '
              'heights.')
        start_height = float(input('What is the initial height? '))
        minimum_height = float(input('What is the reached height? '))

    if minimum_height == 0:
        return infinite_sum(efficiency, start_height, minimum_height,
                            gravitational_constant=GRAVITATIONAL_CONSTANT)

    return finite_sum(efficiency, start_height, minimum_height,
                      gravitational_constant=GRAVITATIONAL_CONSTANT)


def infinite_sum(efficiency, start_height, minimum_height,
                 gravitational_constant=GRAVITATIONAL_CONSTANT):
    """
    Computes the infinite geometric sum for the time taken when the
    minimum_height = 0.

    Parameters
    ----------
    efficiency : float, coefficient giving the energy lost at each bounce.
    start_height : float, height at which the ball is dropped.
    minimum_height : float, height above which the number of bounces is
    calculated.
    gravitational_constant : float, acceleration on Earth.

    Returns: distance_travelled()
    """
    time_drop = np.sqrt((2*start_height)/gravitational_constant)
    total_time = 2*time_drop/(1-np.sqrt(efficiency)) - time_drop

    number_bounces_plus_drop = 'infinitely many'

    return distance_travelled(efficiency, start_height, minimum_height,
                              total_time, number_bounces_plus_drop)


def finite_sum(efficiency, start_height, minimum_height,
               gravitational_constant=GRAVITATIONAL_CONSTANT):
    """
    Computes the finite geometric sum for the time taken when the
    minimum_height = 0.

    Parameters
    ----------
    efficiency : float, coefficient giving the energy lost at each bounce.
    start_height : float, height at which the ball is dropped.
    minimum_height : float, height above which the number of bounces is
    calculated.
    gravitational_constant : float, acceleration on Earth.

    Returns: distance_travelled()
    """
    current_height = start_height
    number_bounces_plus_drop = 0

    while minimum_height < current_height:
        current_height *= efficiency
        number_bounces_plus_drop += 1

    time_drop = np.sqrt((2*start_height)/gravitational_constant)
    total_time = 2*time_drop*(((np.sqrt(efficiency**number_bounces_plus_drop))
                               - 1)/(np.sqrt(efficiency)-1)) - time_drop

    return distance_travelled(efficiency, start_height, minimum_height,
                              total_time, number_bounces_plus_drop)


def distance_travelled(efficiency, start_height, minimum_height, total_time,
                       number_bounces_plus_drop):
    """
    Asks for user input if they want to know the distance travelled by the
    ball, calculates it and outputs it.

    Parameters
    ----------
    efficiency : float, coefficient giving the energy lost at each bounce.
    start_height : float, height at which the ball is dropped.
    minimum_height : float, height above which the number of bounces is
    calculated.
    number_bounces_plus_drop : float, number of bounces of the ball above the
    minimum height + drop.
    total_time: float, time taken by the ball to do its bounces.

    Returns: output()
    """

    distance_input = input('Do you want to know the total distance travelled '
                           'by the ball? (Y or N) ')
    if distance_input == 'Y':
        distance_drop = start_height
        if minimum_height == 0:
            total_distance = 2*distance_drop/(1-efficiency)-distance_drop

        else:
            distance_drop = start_height
            total_distance = 2*distance_drop
            total_distance *= ((efficiency**number_bounces_plus_drop-1)
                               / (efficiency-1))-distance_drop

        print('\nThe ball has travelled a distance of {0:.2f} '
              'meters'.format(total_distance))

    return output(minimum_height, number_bounces_plus_drop, total_time)


def output(minimum_height, number_bounces_plus_drop, total_time):
    """
    Outputs the number of bounces and the time taken.

    Parameters
    ----------
    minimum_height : float, height above which the number of bounces is
    calculated.
    number_bounces_plus_drop : float, number of bounces of the ball above the
    minimum height + drop.
    total_time: float, time taken by the ball to do its bounces.

    Returns: number_bounces and total_time
    """
    if minimum_height == 0:
        number_bounces = number_bounces_plus_drop
    else:
        number_bounces = number_bounces_plus_drop - 1

    return print('\nThe ball has bounced {0} time(s) in {1:.2f}'
                 ' seconds.'.format(number_bounces, total_time))


user_input()
