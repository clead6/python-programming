# -*- coding: utf-8 -*-

"""
PHYS20161 Week 1 quiz: Order lines 1 - weight

Lloyd Cawthorne 30/05/19

This code calculates the weight of an object given its mass in kg.
For it to work, you must put the lines in the correct order.
Once it is working,select the order from the options on Blackboard.

"""

MASS = float(input('What is the mass of the object in kg? '))  # line A
print('A mass of ', MASS, ' kg has a weight of ', WEIGHT, ' N.')  # line B
WEIGHT = MASS * 9.81  # line C
