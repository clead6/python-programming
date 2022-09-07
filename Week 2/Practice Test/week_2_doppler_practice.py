# -*- coding: utf-8 -*-
"""
PHYS20161 week 1 - Debug 3 errors in functions: Doppler shift

This code finds the speed of an observer given how far they travel in a time
then calculates the observed frequency they would hear a stationary sound at.

Correct three errros in the functions then copy the full output into BB.

Lloyd Cawthorne 13/09/19

"""
# SI units

DISTANCE = 17.4587
TIME = 2.34879
EMITTED_FREQUENCY = 13569.7845


def speed_function(distance, time):
    """Calculates speed a assuming linear relationship between distance and
    time.

    distance (float)
    time (float)
    """
    speed_calculated = distance / time

    return speed_calculated


def observed_frequency_function(speed, emitted_frequency):
    """Returns observed frequency given speed of observer and emmitted
    frequency.

    speed (float)
    emitted_frequency (float)
    """
    speed_of_sound = 343.0

    observed_frequency = (1.0 + speed / speed_of_sound) * emitted_frequency

    return observed_frequency


OBSERVED_FREQUENCY = observed_frequency_function(
        speed_function(DISTANCE, TIME), EMITTED_FREQUENCY)

print('The moving observer hears a', OBSERVED_FREQUENCY, 'Hz sound.')
