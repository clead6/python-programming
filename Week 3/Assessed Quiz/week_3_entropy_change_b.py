# -*- coding: utf-8 -*-
"""
PHYS20161 quiz change in entropy B

This code calculates the change in entropy of the Universe when an object at
an initial_temperature is dropped, irreversibly, from a height into a lake
(heat bath) at a lower final_temperatur.

Run this code, as is, through the linter and select the correct score on
BlackBoard.

Lloyd Cawthorne 11/02/20
"""
import numpy as np

# SI units

c = 129.0

g = 9.81


def Delta_S_Obj(MASS, T_i, T_f):
    """
    Returns the entropy change of the object (float) after being
    irreversibly cooled down.
    Args:
        MASS (float)
        T_i (float)
        T_f (float)
    """

    return (MASS * c * np.log(T_f / T_i))


def Delta_S_Lak(m, T_i, T_f):
    """
    Returns the entropy change of the lake (float) from cooling down the
    object.
    Args:
        m (float)
        T_i (float)
        T_f (float)
    """

    DeltaQ = m * c * (T_i - T_f)

    return DeltaQ / T_f


def Delta_S_Grav(m, h, T):
    """
    Returns the change in entropy (float) due to the object being dropped from
    some height.
    Args:
        m (float)
        h (float)
        T (float)
    """

    return m * g * h / T


def Delta_S_Tot(m, T_i, T_f, h):
    """
    Returns the total change in entropy (float) from the object being dropped
    irreversibly from a height into a lake at a colder temperature.
    Args:
        m (float)
        T_i (float)
        T_f (float)
        h (float)
    """

    return (Delta_S_Obj(m, T_i, T_f) + Delta_S_Lak(m, T_i, T_f)
            + Delta_S_Grav(m, h, T_f))
