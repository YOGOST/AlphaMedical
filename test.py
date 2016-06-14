# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 17:14:59 2016

@author: Jubin
using 3 diseases datasets to run cross validation many times for Naive Bayes and Decision Tree algorithm
"""

import classifier as clf
import numpy as np

def cro_vld(clf, k):
    '''
    some one classifier need to be run k times
    
    Returns
    -------
    y_hat: the array of predicted result        
    '''    
    
    y_hat = nb_clf.classify()    #get the first result to define the row size of array
    row_len = np.shape(y_hat)[0]
    for i in range(0, k-2):
        rst = nb_clf.classify()
        y_hat = np.append(y_hat, rst)
        
    col_len = len(y_hat)/k
    y_hat = y_hat.reshape((row_len, col_len))  
    
    return y_hat      
        
    
    
    
def plot(nb_y, nb_y_hat, tree_y, tree_y_hat):
    '''
    Parameters
    ----------
    nb_y: the real labels of diseases, which is a one dimension array
    nb_y_hat: the predicted labels of diseases, which is a matrix
    and so on
    '''   
    
    
    
    
    
if __name__ == '__main__':
    nb_clf = clf.Classifier('NB')
    tree_clf = clf.Classifier('Tree')
    
    nb_y_hat = cro_vld(nb_clf, 10)
    tree_y_hat = cro_vld(tree_clf, 10)
    
    plot(nb_clf.y, nb_y_hat, tree_clf.y, tree_y_hat)

