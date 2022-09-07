# -*- coding: utf-8 -*-
"""
PHYS20161 quiz PyLint PRACTICE relativistic velocities C


Lloyd Cawthorne 03/04/20
"""
import numpy as np

c = 3*10**8

def lf(v):
    
    return 1. / np.sqrt(1 - v**2 / c**2)


def vx(vxp, v):

    return ((vxp + v) / (1 + v * vxp / c**2))


def vp(vpp , vxp , v):

    g = lf(v)

    return vpp / (g * (1 + v * vxp / c**2))


def vb(vps, v):

    vxp = vps[0]
    vyp = vps[1]
    vzp = vps[2]

    vup = [vx(vxp, v), vp(vyp, vxp, v), vp(vzp, vxp, v)]
    return vup
