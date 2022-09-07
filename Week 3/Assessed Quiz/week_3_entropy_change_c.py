# -*- coding: utf-8 -*-
"""
PHYS20161 quiz change in entropy C

This code calculates the change in entropy of the Universe when an object at 
an initial_temperature is dropped, irreversibly, from a height into a lake
(heat bath) at a lower final_temperatur.

Run this code, as is, through the linter and select the correct score on
BlackBoard.

Lloyd Cawthorne 11/02/20
"""
import numpy as np 

# SI units

HEAT_CAPACITY = 129.0
G_CONSTANT = 9.81
HEAT_EXCHANGE = 0.0 


def entropy_change_object(mass, initial_temperature, final_temperature):
    """
    Returns the entropy change of the object (float) after being
    irreversibly cooled down.
    Args:
        mass (floaT)
        initial_temperature (float)
        final_temperature (float)
    """
    
    return (mass * HEAT_CAPACITY * np.log(final_temperature
                                          / initial_temperature))


def entropy_change_lake(object_mass, inital_temperature, final_temperature):
    """
    Returns the entropy change of the lake (float) from cooling down the
    object.
    Args:
        object_mass (float)
        initial_temperature (float)
        final_temperature (float)
    """
    
    HEAT_EXCHANGE = object_mass * HEAT_CAPACITY * (inital_temperature 
                                                   - final_temperature)

    return HEAT_EXCHANGE / final_temperature 


def entropy_change_drop(mass, height, final_temperature): 
    """
    Returns the change in entropy (float) due to the object being dropped from
    some height.
    Args:
        mass (float)
        height (float)
        final_temperature (float)
    """
    
    return mass * G_CONSTANT * height / final_temperature


def total_entropy_change(mass, initial_temperature, final_temperature, height):
    """
    Returns the total change in entropy (float) from the object being dropped
    irreversibly from a height into a lake at a colder temperature.
    Args:
        mass (float)
        initial_temperature (float)
        final_temperature (float)
        height (float)
    """

    return (entropy_change_object(mass, initial_temperature, final_temperature) 
            + entropy_change_lake(mass, initial_temperature, final_temperature) 
            + entropy_change_drop(mass, height, final_temperature)) 
