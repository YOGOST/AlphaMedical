# -*- coding: utf-8 -*-
"""
Created on Sun Apr 24 19:08:42 2016

@author: Administrator
"""

import numpy as np
from scipy import linalg

A = np.array([[1,2],[3,4]])
print(linalg.inv(A))