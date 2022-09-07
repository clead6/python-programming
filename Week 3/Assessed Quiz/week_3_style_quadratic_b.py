# -*- coding: utf-8 -*-
"""
PHYS20161 week 3 style quiz 1 B

Function solves quadratic equation given input parameters.

See instructions on BB on how to answer the question.

Lloyd Cawthorne 26/09/19

"""


def quad_sol(a, b, c):
    """
    Solves ax^2 + bx + c = 0
    Outputs two possible results

    a (float, non zero)
    b (float)
    c (float)
    """

    #  Goes into square root
    term = b**2 - 4 * a * c

    if term < 0:
        # Exit if no sols
        return print('No real solutions.')
    else:
        # solutions given by s1 and s2
        s1 = (-b + term**0.5) / (2. * a)
        s2 = (-b - term**0.5) / (2. * a)

        return print('The solutions are {0:g} and {1:g}.'
                     .format(s1, s2))
