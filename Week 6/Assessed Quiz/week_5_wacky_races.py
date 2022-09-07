# -*- coding: utf-8 -*-
"""
PHYS20161 Week 6 - Wacky Races

Lloyd Cawthorne 18/10/19

This code tracks the position of a three contestants competeing in a Wacky Race
(https://en.wikipedia.org/wiki/Wacky_Races_(1968_TV_series))

Given a time in seconds, ranke_at_time finds the position of the racers to the
nearest minute.

It is a very close race, if it were cutshort at any time (or length) then the
 outcome would be different.

Note: We are showcasing a variety of methods here, some of which are
equivalent.

Correct 10 bugs then select the correct answers from Blackboard accordingly.

"""

import numpy as np

# Constants; SI units

INTERVAL = 60
UPPER_TIME_LIMIT = 3600

# Peter Pefect: uniform acceleration approaching max speed
PETER_PERFECT_MAX_SPEED = 40

# Penelope Pitstop, engine problems so velocity randomly varies every 60 second
PENELOPE_PITSTOP_VELOCITIES = np.array([2.0, 73.0, 71.0, -5.0, 47.0, 13.0,
                                        35.0, -15.0, 11.0, 30.0, -2.0, 54.0,
                                        3.0, 77.0, -5.0, 29.0, 4.0, 16.0,62.0,
                                        17.0, 80.0, 5.0, 37.0, 36.0, 59.0,
                                        64.0, 47.0, 35.0, 52.0, -9.0, 10.0,
                                        23.0, -6.0, 29.0, 8.0, 80.0,64.0, 17.0,
                                        76.0, 38.0, 33.0, 48.0, 52.0, 74.0,
                                        68.0, -11.0, 20.0, 4.0, 3.0, -12.0,
                                        13.0, -14.0, 35.0,-9.0, 3.0, 24.0,
                                        -8.0, 35.0, 41.0, 1.0])

# Dick Dastardly, head start (cheats) but series of blunders leads to
# erratic motion.

# This is split into 5 curves which must be concatenated

DICK_DASTARDLY_1 = np.array([[39952., 0],  [40201.8, 60], [41190.5, 120],
                             [42163., 180], [43943.1, 240], [45475.2, 300],
                             [47051.5, 360], [48602.4, 420], [50253.3, 480],
                             [52792.5, 540], [54946.9, 600], [56894.7, 660],
                             [59574.6, 720], [61638.2, 780], [64577.5, 840],
                             [66790., 900], [69650.5, 960]])
DICK_DASTARDLY_2 = np.array([[71618, 1020], [71600, 1080], [71596, 1140],
                             [71004, 1200], [71025, 1260], [70840, 1320],
                             [70999, 1380], [70888, 1440], [70373, 1500],
                             [70634, 1560], [70542, 1620], [70544, 1680],
                             [70347, 1740], [69971, 1800], [70128, 1860],
                             [69505, 1920], [69403, 1980], [69436, 2040],
                             [69389, 2100], [69372, 2160], [69448, 2220],
                             [68774, 2280], [69013, 2340], [68593, 2400],
                             [68466, 2460]])
DICK_DASTARDLY_3 = np.array([[69025.2, 2520], [70488.7, 2580], [72445.3, 2640],
                             [75387.8, 2700], [78689., 2760], [82528.7, 2820],
                             [87204.9, 2880], [91609.4, 2940],
                             [97454.8, 3000]])
DICK_DASTARDLY_4 = np.array([[102339, 3060], [103526, 3120], [97441, 3180]])
DICK_DASTARDLY_5 = np.array([[92306.1, 3240], [91293.3, 3300], [90867.5, 3360],
                             [90451.3, 3420], [90330.7, 3480], [90403.5, 3540],
                             [90084.9, 3600]])

# Function definitions


def peter_perfect_distance_function(time_input,
                                    max_speed=PETER_PERFECT_MAX_SPEED):

    """Returns distance (float) from gradual acceleration to max speed.

    max_speed (float)
    time_input (float)
    """
    distance = ((-800 + np.exp(-0.05 * np.sqrt(time_input))
                 * (800 + max_speed * np.sqrt(time_input)) + time_input)
                * max_speed)
    return distance


def penelope_pitstop_displacement_per_interval(velocity):

    " Computes x  = v t for a given velocity and time interval"

    displacement = velocity * INTERVAL
    return displacement


def is_float(number):
    """Checks if input is valid

    Returns True if number is float.
    """

    try:
        float(number)
        return True

    except ValueError:
        return False


def validate_time_input(time_input):
    """
    Validates time_input which should be a float between 0 and
    UPPER_TIME_LIMIT.
    Outputs 0 or 1 depending on if criteria are met.
    """
    if is_float(time_input):
        if 0 <= time_input <= UPPER_TIME_LIMIT:
            print('After ', time_input, 'seconds...')
            return 1

        print('Please enter a time between 0 and 3600 seconds.')
        return 0

    print("Invalid input, check argument is a float.")
    return 0


def locate_by_index(time_input, distance_time_array):
    """
    Finds the first entry in the array given where the time element is greater
    than or equal to the input. Outputs the corresponding index (int).

    time_input (float)
    distance_time_array [distance (float), time (float)]
    """

    index = 0

    for time_value in distance_time_array[:, 1]:
        if time_value <= time_input:
            break
        index += 1

    return index


def locate_by_distance(time_input, distance_time_array):
    """
    Given a time and list of distances, searches for index that gives the time
    closest to the input.
    Args:
        time_input (float)
        distance_time_array [time, distance]; [float, float]
    Returns:
        pitstop_index (int)
    """
    # Search Pitstop array for time within 30 seconds of time given
    index = 0
    found = True

    is_close = []

    for time_value in distance_time_array[:, 1]:
        is_close.append(time_input - INTERVAL/2 <= time_value < (time_input
                                                                 + INTERVAL/2)
                        )

    # Find location of entry to be used

    while found == True:
        if is_close[index]:
            found = False

        else:
            index += 1

    return index


def list_positions(perfect_distance, pitstop_distance, dastardly_distance):
    """
    Given each driver's postion at a particular time,
    sorts them and prints the order.

    All inputs are floats

    Returns a list in order from first to last of each driver's name (string)
    and their distance in metres (float).
    """
    # Join and sort positions
    names = ['Peter Perfect', 'Penelope Pitstop', 'Dick Dastardly']

    distances = [perfect_distance, pitstop_distance,
                 dastardly_distance]

    positions = []

    for index, name in enumerate(names):
        positions.append([name, distances[index]])

    rank = sorted(positions, key=lambda x: x[1], reverse=True)

    # Print positions

    counter = 1

    for driver in rank:

        print('In position {0:1d} is '.format(counter)
              + driver[0], 'who is {0:^6.0f} m away from the start.'
              .format(driver[1]))

        counter += 1

    return rank


def rank_at_time(time, perfect_distances, pitstop_distances,
                 dastardly_distances):
    """For a given time, in seconds, returns the race order.
    Checks if input is valid and chooses appropriate bound of intermediate
    times.
    How this is done is different for each driver.

    time (float)
    perfect_distances [time, distance]; [float, float]
    pitstop_distances [time, distance]; [float, float]
    dastardly_distances [time, distance]; [float, float]
    """

    if not validate_time_input(time):
        return 1

    # Round time in minutes and set to integer so it can be used as an index
    minutes = int(np.round(int(time) / INTERVAL))

    # Find position of Perfect using index

    peter_perfect_distance = perfect_distances[minutes, 0]

    pitstop_index = locate_by_distance(time, pitstop_distances)
    penelope_pitstop_distance = pitstop_distances[pitstop_index][0]

    dastardly_index = locate_by_index(time, dastardly_distances)
    dick_dastardly_distance = dastardly_distances[dastardly_index, 0]

    positions = list_positions(peter_perfect_distance,
                               penelope_pitstop_distance,
                               dick_dastardly_distance)
    return positions


# Main code

# These variables are manipulated so we keep them in snake_case. Given length
# of code this will only be a small deduction in code analysis score.

times = np.arange(0.0, 3660.0, 60)

# ~~~~~~~~~~~~~~Peter Perfect distances~~~~~~~~~~~~~~

# Initialise array with coreect number of collumns ready to append to.
# Could use np.empty or .reshape
peter_perfect_distances = np.zeros((0, 2))

for time_element in times:
    temp = np.array([peter_perfect_distance_function(time_element),
                     time_element])
    peter_perfect_distances = np.vstack([peter_perfect_distances, temp])

# ~~~~~~~~~~~~~~Penelope Pitstop Distances~~~~~~~~~~~~~~

# Calculate each displacement
penelope_pitstop_displacements = penelope_pitstop_displacement_per_interval(
    PENELOPE_PITSTOP_VELOCITIES)

# Use inbuilt numpy function to find distance at each interval
penelope_pitstop_distances = np.cumsum(penelope_pitstop_displacements)

# Add start position
penelope_pitstop_distances = np.append(0, penelope_pitstop_distances)

# Include times; convert arrays into len(array) by 1 2D arrays, then use hstack

times_reshaped = times.reshape(len(times), 1)
penelope_pitstop_distances_reshaped = penelope_pitstop_distances.reshape(
        len(penelope_pitstop_distances), 1)

penelope_pitstop_distances = np.hstack((penelope_pitstop_distances_reshaped,
                                        times_reshaped))

# ~~~~~~~~~~~~~~Dick Dastardly distances~~~~~~~~~~~~~~

dick_dastardly_distances = np.concatenate((DICK_DASTARDLY_1, DICK_DASTARDLY_2,
                                           DICK_DASTARDLY_3, DICK_DASTARDLY_4,
                                           DICK_DASTARDLY_5), axis=0)
time = 3400.
rank_at_time(time, peter_perfect_distances, penelope_pitstop_distances,
                 dick_dastardly_distances)