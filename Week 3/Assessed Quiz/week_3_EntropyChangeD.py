# -*- coding: utf-8 -*-
"""
PHYS20161 quiz change in entropy D

This code calculates the change in entropy of the Universe when an object at
an initial_temperature is dropped, irreversibly, from a height into a lake
(heat bath) at a lower final_temperatur.

Run this code, as is, through the linter and select the correct score on
BlackBoard.

Lloyd Cawthorne 11/02/20
"""
import numpy as np

# SI units

G_CONSTANT = 9.81


def EntropyChangeObject(m, initial_temperature, final_temperature):
    """
    Returns the entropy change of the object (float) after being
    irreversibly cooled down.
    Args:
        m (float)
        initial_temperature (float)
        final_temperature (float)
    """
    C = 129.0
    hc = m*C

    return hc * np.log(final_temperature / initial_temperature)


def EntropyChangeLake(m, inital_temperature, final_temperature):
    """
    Returns the entropy change of the lake (float) from cooling down the
    object.
    Args:
        m (float)
        initial_temperature (float)
        final_temperature (float)
    """
    C = 129.0
    hc = m*C
    delta_q = hc * (inital_temperature - final_temperature)

    return delta_q / final_temperature


def EntropyChangeDrop(m, height, final_temperature):
    """
    Returns the change in entropy (float) due to the object being dropped from
    some height.
    Args:
        m (float)
        height (float)
        final_temperature (float)
    """

    return m * G_CONSTANT * height / final_temperature


def TotalEntropyChange(m, initial_temperature, final_temperature, height):
    """
    Returns the total change in entropy (float) from the object being dropped
    irreversibly from a height into a lake at a colder temperature.
    Args:
        m (float)
        initial_temperature (float)
        final_temperature (float)
        height (float)
    """

    return (EntropyChangeObject(m, initial_temperature, final_temperature)
            + EntropyChangeLake(m, initial_temperature, final_temperature)
            + EntropyChangeDrop(m, height, final_temperature))
