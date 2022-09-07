# -*- coding: utf-8 -*-
"""
PHYS20161 quiz PyLint PRACTICE relativistic velocities B

This code calculates velocities observed in an inertial frame given the
speed of a frame where velocities-primed have been measured.

Run this code, as is, through the linter and select the correct score on
BlackBoard.

Lloyd Cawthorne 03/04/20
"""
import numpy as np

# SI units

SPEED_OF_LIGHT=3*10**8


def lorentz_factor(frame_speed):
    """
    Returns Lorentz factor (float) for a given speed (float).
    """

    return 1./np.sqrt(1-frame_speed**2/SPEED_OF_LIGHT**2)


def x_speed(x_speed_primed,frame_speed):
    """
    Returns the speed in the x direction given the speed in the primed frame
    and the speed of that frame.
    Args:
        x_speed_primed (float)
        frame_speed (float)
    """

    return ((x_speed_primed+frame_speed)/(1+frame_speed*x_speed_primed/SPEED_OF_LIGHT**2))


def perpendicular_speed(speed_primed,x_speed_primed,frame_speed):
    """
    Returns the speed in the direction perpendicular to x (y or z) given the
    speed in the primed frame and the speed of that frame.
    Args:
        speed_primed (float)
        x_speed_primed (float)
        frame_speed (float)
    """

    gamma=lorentz_factor(frame_speed)

    return speed_primed/(gamma*(1+frame_speed*x_speed_primed/SPEED_OF_LIGHT**2))


def boosted_velocity(velocity_primed,frame_speed):
    """
    Returns the boosted velocity in the unprimed frame [(float)].
    Args:
        velocity [float, float, float]
        frame_speed (float)
    """
    x_speed_primed=velocity_primed[0]
    y_speed_primed=velocity_primed[1]
    z_speed_primed=velocity_primed[2]
    velocity=[x_speed(x_speed_primed,frame_speed),perpendicular_speed(y_speed_primed,x_speed_primed,frame_speed),perpendicular_speed(z_speed_primed,x_speed_primed,frame_speed)]
    return velocity
