# -*- coding: utf-8 -*-
"""
Created on Tue May 31 12:56:18 2016

Created by Jubin on 2016-6-12
对3种疾病的特征数据进行贝叶斯分类和决策树分类，并比较效果
"""

import pickle as pk
import numpy as np
import random
from sklearn.naive_bayes import BernoulliNB
from sklearn import tree


#load data
class Classifier(object):
    
    def __init__(self, typeStr):
        '''
        X refer to the trainset, Y refer to the target label of X, x refer to data in testset, and
        y refer to the real label in testset, y_hat refer to the predicted label            
        
        Parameters
        ----------
        typeStr: specify the type of classifier         
        
        '''         
        self.X, self.Y, self.x, self.y = self.load_data()
        self.typeStr = typeStr
        self.y_hat = np.zeros(len(self.y))
        
        
    def load_data(self, tarin_test_sepa=.9):
        '''
        Parameters
        ----------
        tarin_test_sepa: the proportion of trainset         
        
        '''        
        
        with open('./data/patients_matrix.pickle', 'rb') as f:
            patients_matrix_std = pk.load(f)
            target = pk.load(f)
            #features = pk.load(f)
            #randomly separate the patients matrix by row
            randint_1 = random.randint(0, 9)
            randint_2 = random.randint(10, 19)
            randint_3 = random.randint(20, 29)
            
            x = patients_matrix_std[randint_1,:]            
            y = np.array(target[randint_1])            
            x = np.append(x, patients_matrix_std[randint_2,:])
            y = np.append(y, target[randint_2])
            x = np.append(x, patients_matrix_std[randint_3,:])
            y = np.append(y, target[randint_3])   

            patients_matrix_std = np.delete(patients_matrix_std, [randint_1, randint_2, randint_3], 0)
            #patients_matrix_std = np.delete(patients_matrix_std, randint_2, 0)
            #patients_matrix_std = np.delete(patients_matrix_std, randint_3, 0)
            target = np.delete(target, [randint_1, randint_2, randint_3], 0)            
            
            col_len = len(x)/3
            x = x.reshape((3, col_len))
               
            return patients_matrix_std, target, x, y
            
            
            
    def is_multinomial(feature_col, thd):
        '''
        Parameters
        ----------
        feature_col: one dimensional array
        thd: the number of multinomial values and thd must be large than 2
        '''                      
        
        if len(np.unique(feature_col)) <= thd:
            return True
        else:
            return False            
            
            
            
    def is_binomial(feature_col):        
        '''
        Parameters
        ----------
        feature_col: one dimensional array
        '''                      
        
        if len(np.unique(feature_col)) == 2:
            return True
        else:
            return False            
            
            
            
    def classify(self):
        '''
        using default classifiers to train and test  
        
        Returns
        -------
        label: the array of predicted result        
        '''
        
        if self.typeStr == 'NB':
            clf = BernoulliNB()
            clf.fit(self.X, self.Y)  
            self.y_hat = clf.predict(self.x)
        elif self.typeStr == 'Tree':
            clf = tree.DecisionTreeClassifier()
            clf.fit(self.X, self.Y)
            self.y_hat = clf.predict(self.x)
            
        return self.y_hat            
            
            
    def ensemble_classify(self):
        '''
        ensembling NB and Tree classifier for different feature of trainset
        
        Returns
        -------
        label: the array of predicted result        
        '''        
            
                
        
        
            
            


