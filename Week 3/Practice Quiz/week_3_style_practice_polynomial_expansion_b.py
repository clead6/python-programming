# -*- coding: utf-8 -*-
"""
PHYS20161 week 3 style quiz 3 B - polynomial expansion

"""


def factorial(number):
    """
    Returns factorial of number using recursion

    number (int)
    """

    if number <= 1:
        return 1

    return number*factorial(number-1)


def polynomial_expansion(n, sign):
    """
    Returns polynomial expansion, (x +(sign) y)^n as a string.

    n (int, >0)
    sign (+/- 1)
    """

    string=''

    for k in range(n+1):
        coefficient = (int((sign**k)*factorial(n)/(factorial(k)
                                                   *factorial(n-k))))
        string = string+'  {0:+d} x^{1:d} y^{2:d}'.format(coefficient,n-k,k)

    return print(string)
