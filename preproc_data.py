# -*- coding: utf-8 -*-
"""
Created by Jubin on 2016-4-27
create_label()：循环读取目录下excel文件名，建立（文件名，序号值）的标签对
load2matrix()：循环读取目录下excel内容，把原始数据装配到matrix
conv2disc()：把excel中的原始数据转化为离散形式
"""

import xlrd
import numpy as np
import pickle
import sys
import os
import types

def read_parameters():
    args = sys.argv
    if len(args) == 1:
        print('Enter the file_path')
        exit()
    elif len(args) == 2:
        uipath = unicode(args[1], 'utf-8')
        return uipath
    else:
        print('Too many arguments')
        exit()

def open_excel(uifile):
    try:
        data = xlrd.open_workbook(uifile)
        return data
    except Exception, e:
        print str(e)

def create_label():
    uipath = unicode('E:/work/办公室/2016/研究院/黄疸待查/27种疾病', 'utf-8')
    dict_labels = {}
    for fpathe, dirs, fs in os.walk(uipath):
        for f in fs:
            #label = f.split('.')
            dict_labels.setdefault(f, len(dict_labels))

    return dict_labels

def conv2disc(valveStr):
    if len(valveStr) == 0:
        return 0
    elif '轻度' in valveStr:
        return 1
    elif '极重度' in valveStr:
        return 3
    elif '重度' in valveStr:
        return 2
    else:
        return 0

def load2matrix(dict_labels):
    counter = 0
    PRM = np.zeros((450, 270), dtype=int)    #病人记录matrix
    dict_symptons = {}
    dict_patients = {}

    for key, fileNum in dict_labels.items():
        if counter > 100:
            break
        else:
            uipath = unicode('E:/work/办公室/2016/研究院/黄疸待查/27种疾病/', 'utf-8')
            uifile = uipath + key
            print uifile
            data = open_excel(uifile)
            table = data.sheets()[0]
            nrows = table.nrows
            ncols = table.ncols

            for rowNum in range(1, nrows):  #discard the table head
                row = table.row_values(rowNum)
                if row:
                    if not dict_symptons.has_key(row[3]):
                        dict_symptons.setdefault(row[3], len(dict_symptons))
                    row_idx = dict_symptons[row[3]]
                    for colNum in range(5, ncols):  #because the sixth column is the first patient
                        patientIdx_pre = '%d' %fileNum
                        patientIdx_pos = '%d' %(colNum-5)
                        patientIdx_str = patientIdx_pre + '_' + patientIdx_pos
                        if not dict_patients.has_key(patientIdx_str):
                            dict_patients.setdefault(patientIdx_str, len(dict_patients))
                        col_idx = dict_patients[patientIdx_str]
                        value = row[colNum]
                        if type(value) is not types.FloatType:
                            value = conv2disc(value.encode('utf-8'))
                        # if value > 0:
                        #     PRM[row_idx][col_idx] = value
                        #     print('PRM[%d][%d]: %f' %(row_idx, col_idx, value))
        counter += 1

    return PRM

if __name__ == '__main__':
    #print conv2disc('重度')
    #uipath = read_parameters()
    dict_labels = create_label()
    PRL = load2matrix(dict_labels)
    with open('D:/dev/pydev/BetaDoctor/data/raw_matrix.dat', 'wb') as f:
        pickle.dump(PRL, f)

#with open('D:/dev/AliMusic/data/cube_download.dat', 'wb') as f:
#    pickle.dump(CUBE_DOWNLOAD, f)
#with open('D:/dev/AliMusic/data/cube_collect.dat', 'wb') as f:
#    pickle.dump(CUBE_COLLECT, f)
#
#'''
#with open('D:/dev/AliMusic/data/cube_play.dat', 'rb') as f:
#    CUBE_PLAY = pickle.load(f)
#'''
