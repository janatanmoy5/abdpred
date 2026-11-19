#!/usr/bin/env python
# coding: utf-8


# importing required pacakages:
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn import svm
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt  # doctest: +SKIP
from sklearn import datasets, metrics, model_selection, svm
from sklearn.metrics import plot_roc_curve
from sklearn.datasets import load_wine
from sklearn.datasets import load_iris
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2
from sklearn.feature_selection import VarianceThreshold
from sklearn.svm import LinearSVC
from sklearn.datasets import load_iris
from sklearn.feature_selection import SelectFromModel
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
import xgboost as xgb

#importing datasets

dataset = pd.read_csv(r'Training_Testingset2.csv',sep=',')
blindset= pd.read_csv(r'Blind_set_validation.csv',sep=',')


X= dataset.drop('Level',axis=1)
y= dataset['Level']
#X_new = SelectKBest(chi2, k=12).fit_transform(X,y)
#X_new.shape
#sel = VarianceThreshold(threshold=(.8 * (1 - .8)))
#X_new = sel.fit_transform(X)
#lsvc = LinearSVC(C=0.01, penalty="l1", dual=False).fit(X, y)
#model = SelectFromModel(lsvc, prefit=True)
#X_new = model.transform(X)





X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.20, random_state=42)




sc = StandardScaler ()
X_train = sc.fit_transform(X_train)
X_test = sc.fit_transform(X_test)
#X_train[:10]


print ('Performance of Random forest')
rfc = RandomForestClassifier(n_estimators=202, random_state=92)
rfc.fit(X_train,y_train)
pred_rfc=rfc.predict(X_test)
#blind_pred_rfc=rfc.predict (Z)

#pred_rfc[:20]
#pred_rfc
print(classification_report(y_test, pred_rfc))
print(confusion_matrix(y_test, pred_rfc))
#print ("Random Forest classifier: ", rfc.score (X_test, y_test))
from sklearn.model_selection import StratifiedKFold
folds = StratifiedKFold (n_splits=5)
scores_rf =[]
scores_clf=[]
scores_mlpc=[]
scores_xgb=[]
scores_GB_classifier=[]
scores_dtree_clf=[]



#for train_index, test_index in kf.split (X):
    #X_train, X_test, y_train, y_test = X[train_index], X[test_index], y[train_index], y[test_index]
#print (get_score ( RandomForestClassifier(),X_train, X_test, y_train, y_test))

from sklearn.model_selection import cross_val_score
scores_rf.append(cross_val_score (RandomForestClassifier(n_estimators=501, random_state=92, cv=5),X, y))
print ("Random Forest score ",scores_rf)

#scores_clf.append(cross_val_score (SVC(gamma=0.00001, C=2150, coef0=0.05, tol=0.001),X, y))
#print (scores_clf)

#scores_mlpc.append(cross_val_score (MLPClassifier(hidden_layer_sizes=(11, 12, 12), max_iter=700, activation='logistic'),X, y))
#print (scores_mlpc)

#scores_xgb.append(cross_val_score (xgb.XGBClassifier(),X, y))
#print (scores_xgb)

ax = plt.gca()
rfc_disp = plot_roc_curve(rfc, X_test, y_test, ax=ax)
plt.show()

