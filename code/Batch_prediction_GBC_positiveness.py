###############################
## AMDPred Server
## Version 1.0
###############################

import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import KFold
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.metrics import roc_curve, auc
from sklearn import metrics
import pickle
import matplotlib.pyplot as plt
from sklearn.metrics import plot_roc_curve
import sys
import os

currUID = int(sys.argv[1])
directory=currUID
filename="model_GBC_5_fold_pubchem_1_1"
loaded_model = pickle.load(open(filename, 'rb'))
filename2 = (str(directory)+'.csv')

blindset= pd.read_csv(filename2,sep=',')
Z= blindset.drop('Label',axis=1)
z= blindset['Label']

#pred_blind_xgb=loaded_model.predict(Z)
#print (pred_blind_xgb)
#a=pred_blind_xgb.shape
#print (a)
#t=len(pred_blind_xgb)
#print (t)

filename4= (str(directory)+'pos.txt')
filename5= (str(directory)+'neg.txt')
poss=loaded_model.predict_proba(Z)[:,1]
neg=loaded_model.predict_proba(Z)[:,0]
t=len(poss)
t1=len(neg)

for j in range(t):
    
    f = open(filename4, "a")
    f.write(str(poss[j]))
    f.write("\n")
    f.close()

for k in range(t1):
    f = open(filename5, "a")
    f.write(str(neg[k]))
    f.write("\n")
    f.close()


