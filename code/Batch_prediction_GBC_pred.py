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

pred_blind_xgb=loaded_model.predict(Z)
a=pred_blind_xgb.shape
t=len(pred_blind_xgb)
#print (t)
filename3 = (str(directory)+'pred.txt')



for i in range(t):
    
    if pred_blind_xgb[i]==1:
        f = open(filename3, "a")
        f.write("pos\n")
        #f.write("\n")
        f.close()
    else:
        f = open(filename3, "a")
        f.write("neg\n")
        #f.write("\n")
        f.close()


