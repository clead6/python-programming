# -*- coding: utf-8 -*-
"""
PHYS20161 quiz PyLint PRACTICE relativistic velocities A

This code calculates velocities observed in an inertial frame given the
speed of a frame where velocities-primed have been measured.

Run this code, as is, through the linter and select the correct score on
BlackBoard.

Lloyd Cawthorne 03/04/20
"""
import numpy as np

# SI units

SPEED_OF_LIGHT = 3*10**8

def Lorentz_Factor(frame_speed):
    """
    Returns Lorentz factor (float) for a given speed (float).
    """

    return 1. / np.sqrt(1 - frame_speed**2 / SPEED_OF_LIGHT**2)


def X_Speed(x_speed_primed , frame_speed):
    """
    Returns the speed in the x direction given the speed in the primed frame
    and the speed of that frame.
    Args:
        x_speed_primed (float)
        frame_speed (float)
    """

    return ((x_speed_primed + frame_speed)
            / (1 + frame_speed * x_speed_primed / SPEED_OF_LIGHT**2))

def Perpendicular_Speed(speed_primed , x_speed_primed , frame_speed):
    """
    Returns the speed in the direction perpendicular to x (y or z) given the
    speed in the primed frame and the speed of that frame.
    Args:
        speed_primed (float)
        x_speed_primed (float)
        frame_speed (float)
    """

    gamma = Lorentz_Factor(frame_speed)

    return speed_primed / (gamma * (1 + frame_speed * x_speed_primed
                                    / SPEED_OF_LIGHT**2))

def Boosted_Velocity(velocity_primed , frame_speed):
    """
    Returns the boosted velocity in the unprimed frame [(float)].
    Args:
        velocity [float, float, float]
        frame_speed (float)
    """
    x_speed_primed = velocity_primed[0]
    y_speed_primed = velocity_primed[1]
    z_speed_primed = velocity_primed[2]

    velocity = [X_Speed(x_speed_primed, frame_speed),
                Perpendicular_Speed(y_speed_primed, x_speed_primed,
                                    frame_speed),
                Perpendicular_Speed(z_speed_primed, x_speed_primed,
                                    frame_speed)]
    return velocity
