# -*- coding: utf-8 -*-
"""
PHYS20161 Week 8 quiz Intro to matplotlib

This code is setup to produce a plot.

Select the correct options on BlackBoard to produce the plot displayed.

Lloyd Cawthorne 29/10/19

"""

import matplotlib.pyplot as plt
import numpy as np

# Code goes here
X_VALUES = np.linspace(-2, 2, 1000)
plt.title('Figure 1', fontsize=15, fontname='Times New Roman')
plt.xlabel('x', color='purple')
plt.ylabel('Functions', fontsize=12, fontname='Comic Sans MS')
plt.plot(X_VALUES, np.cos( X_VALUES), label='cos(x)', c='blue', dashes=[8, 4, 2, 4])
plt.plot(X_VALUES, 1 - X_VALUES**2 / 2, label='1-x^2/2', c='red', linewidth=5)
plt.xlim(-2, 2)
plt.grid(True, axis='y', color='black')
plt.grid(True, axis='x', color='green', linewidth=2)
plt.legend(loc='best')

plt.savefig('plot.png', dpi=300)

plt.show()
