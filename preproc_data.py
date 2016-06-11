# -*- coding: utf-8 -*-
"""
Created by Jubin on 2016-4-27
create_label()：循环读取目录下excel文件名，建立（文件名，序号值）的标签对
load2matrix()：循环读取目录下excel内容，把原始数据装配到matrix
conv2disc()：把excel中的原始数据转化为离散形式
"""

import xlrd, xlwt
import pickle
import sys
import numpy as np
from sklearn.feature_extraction import DictVectorizer
from sklearn.feature_selection import VarianceThreshold
from sklearn import preprocessing
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2


def read_parameters():
    args = sys.argv
    if len(args) == 1:
        print('Enter the file_path')
        exit()
    elif len(args) == 2:
        uipath = args[1]
        uipath.encode('UTF-8', errors='strict')
        return uipath
    else:
        print('Too many arguments')
        exit()
        
        

def open_excel(uifile):
    try:
        data = xlrd.open_workbook(uifile)
        return data
    except Exception as e:
        print('open file error:'.format(e))
        
   
    
def load2list(uifile):
    '''
    load sample from ./data/3.xls into patients list, every element
    is a dictionary of patient which contain all raw features.
    '''
    
    data = open_excel(uifile)    
    table = data.sheets()[0]
    ncols = table.ncols
    raw_features = table.col_values(3)  #得到专家确定的特征，位于原始excel的第4列    
    del(raw_features[0])
    features_len = len(raw_features)
    patients = []
    for i in range(5, ncols-1):    #把每个列sample装配到list的元素，并与feature（第四列）对齐
        sample = table.col_values(i)
        del(sample[0])
        patient = {}
        for j in range(features_len):
            patient.setdefault(raw_features[j], sample[j])
            #patient[raw_features[j]] = sample[j]
            #print(raw_features[j], sample[j])
        
        patients.append(patient)
    
    return patients
    
    
    
def conv2matrix(patients, sta_type='z-score', sel_type='var', threshold=.8, feature_k=30):
    '''
    extract feature from patient list, all of these features are not real feature, they are preprocessed by expert
    missing value: set 0 when style is 'z-score', and set nan when style is 'min-max'
    binary value feature: 0 means negative, and 1 means positive 
    category value feature: e.g. sex should be regarded one value as one featue 
    real value feature: age should be normalized
    rank value feature: could be set from 1 to n  
    the parameter of type is comprised of 'z-score' and 'min-max' 
    the parameter of threshold is between 0 and 1
    return patients_matrix_std: the standardization of patients matrix
    return features_dict: the dictionary consist of the names and indexes of features will be fed to classifier
    '''    
    
    #process the missing value and the rank value feature
    for i in range(len(patients)):
        for key in patients[i]:
            if patients[i][key] == '':
                patients[i][key] = 0  #process missing value 
            patients[i][key] = rank2int(patients[i][key])   #process rank value feature
    #process the category value feature and convert patients' dictionary to matrix
    vec = DictVectorizer()
    patients_matrix = vec.fit_transform(patients).toarray()          

    #feature selection
    if sel_type == 'var':
        sel = VarianceThreshold(threshold=(threshold * (1 - threshold)))
        patients_matrix_sel = sel.fit_transform(patients_matrix)
    elif sel_type == 'uni':
        y = [1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3]
        sel = SelectKBest(chi2, feature_k)
        patients_matrix_sel = sel.fit_transform(patients_matrix, y)
            
    features_dict = get_features(vec, sel)    
    #print(features_dict)
    
    #feature standardization
    if sta_type == 'z-score':
        patients_matrix_std = preprocessing.scale(patients_matrix)        
    elif sta_type == 'min-max':
        min_max_scaler = preprocessing.MinMaxScaler()
        patients_matrix_std = min_max_scaler.fit_transform(patients_matrix_sel)

    return patients_matrix_std, features_dict
        

    
    
def get_features(vec, sel):
    '''
    parameter of vec contain the features name before feature selection
    parameter of sel is the outcome of feature selection 
    return the dictionary consist of the names and indexes of features will be fed to classifier
    '''    
    #keys = patients_dict.keys()
    features_name_list = vec.get_feature_names() 
    features_idx = sel.get_support(True).tolist()
    features_dict = {}
    
    for i in range(len(features_idx)):
        idx = features_idx[i]
        key = features_name_list[idx]
        #print("the feature_%d selected is: %s" % (idx, key))
        features_dict[key] = idx

    return features_dict    




def save(patients_matrix_std, features_dict):
    with open('./data/patients_matrix.pickle', 'wb') as f:
        pickle.dump(patients_matrix_std, f)
        pickle.dump(features_dict, f)
    

    

def rank2int(valStr):
    if sys.version_info[0] == 2:
        #print(valStr)
        if valStr == '亚临床'.decode('UTF-8'):
            return 1
        elif valStr == '轻度'.decode('UTF-8'):
            return 2
        elif valStr == '极重度'.decode('UTF-8'):
            return 3
        elif valStr == '重度'.decode('UTF-8'):
            return 4
        else:
            return valStr
    elif sys.version_info[0] == 3:
        if valStr == '亚临床':
            return 1
        elif valStr == '轻度':
            return 2
        elif valStr == '极重度':
            return 3
        elif valStr == '重度':
            return 4
        else:
            return valStr
            
        
        
        
def load2matrix(uifile):
    '''
    load ./data/3.xls to matrix        
    '''
      
    data = open_excel(uifile)    
    table = data.sheets()[0]
    nrows = table.nrows
    ncols = table.ncols
    
    patients_matrix = np.zeros((nrows, ncols))    #nrows means feature, ncols means sample  
    for row_idx in range(1, nrows):  #discard the table head
        row = table.row_values(row_idx)
        if row:
            for col_idx in range(5, ncols):  #because the sixth column is the first patient  
                value = row[col_idx]              
                if value > 0:
                    patients_matrix[row_idx][col_idx] = value
                    #print('PRM[%d][%d]: %f' %(row_idx, col_idx, value))
    return patients_matrix



def row_col_trans(uifile):
    '''
    把 excel的行列互换
    '''    
    
    data = open_excel(uifile)    
    table = data.sheets()[0]
    raw_features = table.col_values(3)  #得到专家确定的特征，位于原始excel的第4列
    del(raw_features[0])
    
    new_excel_file = xlwt.Workbook(encoding='utf-8', style_compression=0)
    sheet = new_excel_file.add_sheet('sheet1')    
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = 'Time New Roman'
    style.font = font
    
    for i in range(len(raw_features)):
        #print('feature %d is %s' %(i, raw_features[i]))
        sheet.write(0, i, raw_features[i], style)
    
    new_excel_file.save('./Data/threeDisease.xls')
    
    '''
    print(len(raw_features))
    print(raw_features[0])
    print(table.cell_value(5,6))
    '''

    
'''
def load2matrix(dict_labels):
    counter = 0
    PRM = np.zeros((450, 270), dtype=int)    #病人记录matrix
    dict_symptons = {}
    dict_patients = {}

    for key, fileNum in dict_labels.items():
        if counter > 100:
            break
        else:
            uipath = './data/3种疾病综合'.encode('UTF-8', errors='strict')
            uifile = uipath + key
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
'''    

if __name__ == '__main__':
    patients = load2list('./data/3.xls')
    [patients_matrix_std, features_dict] = conv2matrix(patients, sta_type='min-max', sel_type='var', threshold=.8)
    save(patients_matrix_std, features_dict)
    
    #uipath = read_parameters()
    #row_col_trans('./data/3种疾病综合.xls')
    #PRL = load2matrix(dict_labels)
    #with open('D:/dev/pydev/BetaDoctor/data/raw_matrix.dat', 'wb') as f:
        #pickle.dump(PRL, f)

#with open('D:/dev/AliMusic/data/cube_download.dat', 'wb') as f:
#    pickle.dump(CUBE_DOWNLOAD, f)
#with open('D:/dev/AliMusic/data/cube_collect.dat', 'wb') as f:
#    pickle.dump(CUBE_COLLECT, f)
#
#'''
#with open('D:/dev/AliMusic/data/cube_play.dat', 'rb') as f:
#    CUBE_PLAY = pickle.load(f)
#'''
