# -*- coding: utf-8 -*-
"""
Created on Tue May 31 12:56:18 2016

Created by Jubin on 2016-5-31
create_label()：循环读取目录下excel文件名，建立（文件名，序号值）的标签对
load2matrix()：循环读取目录下excel内容，把原始数据装配到matrix
conv2disc()：把excel中的原始数据转化为离散形式
"""

import sys
import pickle as pk
import numpy as np
import scipy as sp
import sklearn as sl


#load data
class Classifier(object):
    def __init__(self):
        with open('./data/patients_matrix.pickle', 'rb') as f:
            self.patients_matrix_std = pk.load(f)
            self.feature_idx = pk.load(f)


