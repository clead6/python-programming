# -*- coding: utf-8 -*-
"""
PHYS20161 Week 3 quiz - Pell series
Lloyd Cawthorne 27/09/19

This code finds the largest element of the Pell series lower than or equal to
the input given.
(https://en.wikipedia.org/wiki/Pell_number)

Correct 5 bugs to get it working. Then, use the inputs requested in Blackboard.

WARNING: It might run but give incorrect results!

"""


def largest_pell_element(end):
    """
    Returns the largest element (int) of the Pell sequence lower than the
    input given.
    Args:
        end (int)
    """

    # Initial parameters
    p_0 = 0
    p_1 = 1
    p_n = 1

    # Edge case
    if end == 0:
        p_n = 0

    # Standard format of series
    else:
        p_n = 2 * p_1 + p_0

        while p_n <= end:
            # Continuously update parameters accordingly
            p_0 = p_1
            p_1 = p_n
            p_n = 2 * p_1 + p_0

    print('The largest Pell number less than or equal to {0:d} is {1:d}.'
          .format(end, p_1))

    return p_1


END_STRING = input("What is the upper limit for this series? ")
END = int(END_STRING)

largest_pell_element(END)
