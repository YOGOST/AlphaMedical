# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 17:14:59 2016

@author: Jubin
using 3 diseases datasets to run K-fold cross-validation for Naive Bayes and Decision Tree algorithm
"""

import classifier as clf
import numpy as np
from scipy import interp
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc

def cro_vld(clf, k):
    '''
    some one classifier need to be run K-fold cross-validation
    
    Returns
    -------
    y_hat: array, shape=[3, k], the predicted result for 3 diseases        
    '''    
    
    y_hat = nb_clf.classify()    #get the first result to define the row size of array
    col_len = np.shape(y_hat)[0]
    for i in range(0, k-1):
        rst = nb_clf.classify()
        y_hat = np.append(y_hat, rst)
                
    row_len = len(y_hat)/col_len
    y_hat = y_hat.reshape((row_len, col_len))  
    print(y_hat)
    
    return y_hat      
        
    
    
    
def plot_auc(y, y_hat, k):
    '''
    Parameters
    ----------
    y: the real labels of diseases, which is a one dimension array
    y_hat: the predicted labels of diseases, which is a matrix
    k: K-fold cross-validation
    '''   
    
    
    mean_tpr = 0.0
    mean_fpr = np.linspace(0, 1, 100)

    #clf_score 
    clf_score = []
    plt.plot([0, 1], [0, 1], '--', color=(0.6, 0.6, 0.6), label='Luck')
        
    for i in range(0, 2):        
        for j in range(0, k-1):
            fpr, tpr, thresholds = roc_curve(y, clf_score)
            mean_tpr += interp(mean_fpr, fpr, tpr)
            mean_tpr[0] = 0.0            
        
         #roc_auc = auc(fpr, tpr)     
         #mean_tpr /= len(cv)     
         #mean_tpr[-1] = 1.0
        mean_auc = auc(mean_fpr, mean_tpr)            
            
        plt.plot(mean_fpr, mean_tpr, 'k--', label='Mean ROC (area = %0.2f) for diseases %d' % (mean_auc, i), lw=2)
        #plt.legend(loc="lower right")

    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title('ROC and AUC for 3 diseases')    
    plt.show()       
        
    
    
    
if __name__ == '__main__':
    nb_clf = clf.Classifier('NB')
    tree_clf = clf.Classifier('Tree')
    
    nb_y_hat = cro_vld(nb_clf, 10)
    tree_y_hat = cro_vld(tree_clf, 10)
    
    plot_auc(nb_clf.y, nb_y_hat)
    plot_auc(tree_clf.y, tree_y_hat)

