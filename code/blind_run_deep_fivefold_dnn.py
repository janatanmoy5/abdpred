###############################
## AMDPred Server
## Version 1.0
###############################

from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import cross_val_score
from keras.layers import Dense, Dropout, Flatten
from keras.models import Sequential
from keras.layers import Dense
import pandas as pd
from keras import regularizers
from keras.layers import Dense, Dropout, Flatten
from sklearn.model_selection import StratifiedKFold
from tensorflow.keras.losses import sparse_categorical_crossentropy
import warnings  
warnings.filterwarnings('ignore')

from sklearn.model_selection import cross_val_score
from keras import regularizers
from tensorflow import keras
from keras.layers import Dense, Dropout, Flatten
from keras.wrappers.scikit_learn import KerasClassifier
import numpy as np 
import pandas as pd 
import os
from tensorflow.keras.losses import sparse_categorical_crossentropy
from sklearn.preprocessing import StandardScaler
import keras
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
from keras.utils import plot_model  
sns.set()
import matplotlib.pyplot as plt
#import dill as pickle
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix,roc_auc_score, classification_report
from sklearn import metrics
from sklearn.metrics import roc_curve, auc, plot_roc_curve
import pickle
from sklearn.metrics import accuracy_score
import sys
import os


currUID = int(sys.argv[1])
directory=currUID
#print(directory)


new_model = tf.keras.models.load_model('model2')

filename2 = (str(directory)+'.csv')
filename3 = (str(directory)+'DNNpred.txt')
filename4= (str(directory)+'DNNpos.txt')
filename5 = (str(directory)+'DNNneg.txt')



blindset= pd.read_csv(filename2,sep=',')
Z= blindset.drop('Label',axis=1)
z= blindset['Label']
pred_blind_dnn= new_model.predict(Z)
#print (pred_blind_dnn)


pred_blind_dnn = (pred_blind_dnn > 0.55)
f = open(filename3, "a")
f.write(str(pred_blind_dnn))
f.close()
#print (pred_blind_dnn)
proba = new_model.predict_proba(Z)




#print (proba)
if proba < 0.55:
    neg=proba
    #print (neg)
    poss=1-proba
    #print (poss)
    
if proba > 0.55:
    poss=proba
    #print (poss)
    neg=1-proba
    #print (neg)
    
f = open(filename4, "a")
f.write(str(poss))
f.close()
f = open(filename5, "a")
f.write(str(neg))
f.close()  
    
    




