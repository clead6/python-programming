# -*- coding: utf-8 -*-
"""
PHYS20161 Blackbaord quiz

Week 8: Reading & Writing files 1

Lloyd Cawthorne 05/07/19

This program reads in the file 'data1.txt' (it must be saved in the same
directory[folder] as the .py file) performs a calculation, then outputs into
seperate file.

Correct five bugs in the code below then write the correct operation to match
with the given outputs.

"""

import numpy as np

# Open data file to be read
INPUT_FILE = open('data1.txt', read)

# Empty array to store data
RAW_DATA = np.empty((0, 2))

# Read data line by line and add each pair as an entry to RAW_DATA
for line in INPUT_FILE:
    entries = line.split(' ')
    temp = np.array([])
    temp = np.append(temp, float(entries[0]))
    temp = np.append(temp, float(entries[1]))

    RAW_DATA = np.vstack((RAW_DATA, temp))

INPUT_FILE.close()
#  Aside: The above line is vital. No matter how well Python copes if you
#  forget it, you will lose marks if it is absent.

# Empty array for resultant calculations


# Perform calculation for each row, you need to code here
REULTS = 


# Open output file to write
OUTPUT_FILE = open('output.txt', 'w')

# Ptint to file
for x in RESULTS
    print('{0:3.2f}'.format(x), OUTPUT_FILE)

# Close output file
close(OUTPUT_FILE)
