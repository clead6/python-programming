# -*- coding: utf-8 -*-
"""
PHYS20161 Week 3 PRACTICE quiz - Tribonacci series
Lloyd Cawthorne 28/05/19

This code finds the largest element of the tribonacci series lower than the
input given.
The tribonacci series ( http://mathworld.wolfram.com/TribonacciNumber.html ) is
a generalisation of the fiboncci sequence, however, there are three starting
parameters and three numbers are summed for each additional number.

WARNING: It might run but give incorrect results!

"""


def largest_tribonacci_element(end_input):
    """
    Returns the largest element (int) of the Tribonacci sequence lower than the
    input given.
    Args:
        end_input (int)
    """
    # Initial parameters

    n_0 = n_1 = 0
    n_2 = 1

    n = 1

    # Edge case

    if end_input == 0:

        n_2 = 0

    # Standard format of series
    else:

        while n <= end_input:

            # Continuosly update parameters accordingly
            n_0 = n_1
            n_1 = n_2
            n_2 = n
            n = n_0 + n_1 + n_2

    print("The largest element of the tribonacci series less than or equal to "
          "{0:d} is {1:d}.".format(end_input, n_2))

    return n_2


END_STRING = input("What is the upper limit for this series? ")

END = int(END_STRING)

largest_tribonacci_element(END)
