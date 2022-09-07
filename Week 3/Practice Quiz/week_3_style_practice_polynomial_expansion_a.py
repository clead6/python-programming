# -*- coding: utf-8 -*-
"""
PHYS20161 week 3 style quiz 3 A - polynomial expansion

Expands (x + y)^n to a series of n+1 terms and prints result.

Expansion uses binomial coefficients as defined in
(https://en.wikipedia.org/wiki/Binomial_coefficient)

Lloyd Cawthorne 26/09/19
"""


def fact(n):

    if n <= 1:
        return 1

    return n * fact(n - 1)


def binom_coef(n, k):

    coef = fact(n) / (fact(k) * fact(n - k))
    return coef


def print_term(coef, x, y):

    return '  {0:+d} x^{1:d} y^{2:d}'.format(coef, x, y)


def poly_exp(n, pm):

    c_kn = []
    stg = ''

    for k in range(n+1):
        # pm is plus or minus, gives the correct sign
        c_kn.append(int((pm**k) * binom_coef(n, k)))
        # append to a string once each term is calculated.
        stg = stg + print_term(c_kn[k], n - k, k)

    # return print(coefficients)

    return print(stg)
