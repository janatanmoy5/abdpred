###############################
## AMDPred Server
## Version 1.0
###############################

import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
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
#print(directory)




filename="model0_RF_5_fold_pubchem_1_1"
loaded_model = pickle.load(open(filename, 'rb'))
#print (loaded_model)
filename2 = (str(directory)+'.csv')
filename3 = (str(directory)+'RFpred.txt')
filename4= (str(directory)+'RFpos.txt')
filename5 = (str(directory)+'RFneg.txt')
#print (filename2)





blindset= pd.read_csv(filename2,sep=',')
Z= blindset.drop('Label',axis=1)
z= blindset['Label']
result = loaded_model.score(Z,z)
#print(result)
result2=loaded_model.predict(Z)
negativeness= loaded_model.predict_proba(Z)[:,0]
positiveness= loaded_model.predict_proba(Z)[:,1]
#print(result2)

f = open(filename3, "a")
f.write(str(result2))
f.close()
f = open(filename4, "a")
pos=str(positiveness).format()
f.write(pos)
f.close()
f = open(filename5, "a")
neg=str(negativeness).format()
f.write(neg)
f.close()




