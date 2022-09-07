# -*- coding: utf-8 -*-
"""
PHYS20161 Week 3 - Wacky Races PRACTICE

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
PENELOPE_PITSTOP_VELOCITIES = np.array([51.0, 25, -13, -9, 0, 2, 74, 74, 55,
                                        52, 42, 33, 41, 31, 3, 42, 9, 0, 61,
                                        7, 36, -9, 70, 72, -6, 58, 19, 61, 22,
                                        2, 19, 16, 71, 69, 67, 4, 30, -7, 53,
                                        19, 74, -1, 44, 57, -15, 50, 5, 48,
                                        -14, 7, -2, -14, 36, 14, 23, 69, -8,
                                        -3, 41, -8])

# Dick Dastardly, head start (cheats) but series of blunders leads to
# erratic motion.

# This is split into 5 curves which must be concatenated

DICK_DASTARDLY_1 = np.array([[37203., 0], [37198.7, 60], [38033.7, 120],
                             [39076.7, 180], [39646.9, 240], [40700.8, 300],
                             [42364.1, 360], [43349.7, 420], [44977.2, 480],
                             [45866.6, 540], [47896.8, 600], [49021.7, 660],
                             [50732.8, 720], [52554.8, 780], [54257.2, 840],
                             [56147.5, 900], [58261.5, 960]])
DICK_DASTARDLY_2 = np.array([[59111.2, 1020], [59486.2, 1080], [58946.2, 1140],
                             [58816.2, 1200], [58592.2, 1260], [58680.2, 1320],
                             [58754.2, 1380], [58520.2, 1440], [58624.2, 1500],
                             [58225.2, 1560], [58232.2, 1620], [58124.2, 1680],
                             [57869.2, 1740], [57953.2, 1800], [57821.2, 1860],
                             [57535.2, 1920], [57408.2, 1980], [57472.2, 2040],
                             [56949.2, 2100], [56981.2, 2160], [57168.2, 2220],
                             [56970.2, 2280], [56432.2, 2340], [56446.2, 2400],
                             [56603.2, 2460]])
DICK_DASTARDLY_3 = np.array([[56355., 2520], [57897.1, 2580], [60993.8, 2640],
                             [64461.4, 2700], [69020.6, 2760], [74613.1, 2820],
                             [80561.7, 2880], [87460.7, 2940], [95261.2, 3000]
                             ])
DICK_DASTARDLY_4 = np.array([[100316, 3060], [101678, 3120], [95523, 3180]])
DICK_DASTARDLY_5 = np.array([[92395.1, 3240], [91547.3, 3300], [90518.5, 3360],
                             [90350.3, 3420], [90351.7, 3480], [90239.5, 3540],
                             [90225.9, 3600]])

# Function definitions


def peter_perfect_distance_function(time_input,
                                    max_speed=PETER_PERFECT_MAX_SPEED):

    """Returns distance (float) from gradual acceleration to max speed.

    max_speed (float)
    time_input (float)
    """
    distance = ((-987.654 + np.exp(-0.045 * np.sqrt(time_input))
                 * (987.654 + 44.444 * np.sqrt(time_input)) + time_input)
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
        if 0 <= float(time_input) <= UPPER_TIME_LIMIT:
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
    found = False

    is_close = []

    for time_value in distance_time_array[:, 1]:
        is_close.append(time_input - INTERVAL/2 <= time_value < (time_input
                                                                 + INTERVAL/2)
                        )

    # Find location of entry to be used

    while found==False:
        if is_close[index]:
            found = True

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

time = 3200
rank_at_time(time, peter_perfect_distances, penelope_pitstop_distances,
                 dick_dastardly_distances)