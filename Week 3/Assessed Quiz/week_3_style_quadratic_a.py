# -*- coding: utf-8 -*-
"""
PHYS20161 week 3 style quiz 1 A

See instructions on BlackBoard.


"""


def quadratic_solutions(a,b,c):
    """
    Solves ax^2 + bx + c = 0
    Outputs two possible results 

    a (float, non zero)
    b (float)
    c (float)
    """

    sqrt_argument=b**2-4*a*c

    if sqrt_argument<0:
        return print('No real solutions.')
    else:
        solution_1=(-b+sqrt_argument**0.5)/(2.*a)
        solution_2=(-b-sqrt_argument**0.5)/(2.*a)

        return print('The solutions are {0:g} and {1:g}.'
                     .format(solution_1,solution_2))
