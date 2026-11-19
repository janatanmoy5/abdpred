import pubchempy as pcp
from array import *
from pubchempy import Compound
import pandas as pd
import php
import sys
import os
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.ensemble import GradientBoostingClassifier
from sklearn import datasets, metrics, model_selection
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




currUID = int(sys.argv[1])
print ("You have entered CID value: ",currUID)

a=currUID
comp= Compound.from_cid(a)

#Label, mw, xlogp3, hbdc, hdac, rbc, exact_mass, mono_mass, tpsa, hac, charge, complex,isc, dasc, uasc, dbsc, ubsc, cbu


Label=0
mw= comp.molecular_weight
xlogp3= comp.xlogp
hbdc= comp.h_bond_donor_count
hdac= comp.h_bond_acceptor_count 
rbc= comp.rotatable_bond_count 
exact_mass= comp.exact_mass
mono_mass= comp.monoisotopic_mass 
tpsa= comp.tpsa
hac= comp.heavy_atom_count 
charge= comp.charge
complex= comp.complexity 
isc= comp.isotope_atom_count 
dasc= comp.defined_atom_stereo_count 
uasc= comp.undefined_atom_stereo_count 
dbsc= comp.defined_bond_stereo_count
ubsc= comp.undefined_bond_stereo_count 
cbu= comp.covalent_unit_count
#print(mw,",", xl, ",", hbdc,",", hdac,",", rbc, ",", em,",", mm, ",", tp,",", hac, ",", ch, ",", co, ",",isc, ",", dasc, ",",uasc,",",dbsc,",",ubsc,",",cbu)
#descriptor=mw,xl,hbdc,hdac,rbc,em,mm,tp,hac,ch,co,isc,dasc,uasc,dbsc,ubsc,cbu    
print (complex)











import csv

with open('name.csv', 'w') as csvfile:

    #fieldnames =['Label', 'mw', 'xlogp3', 'hbdc', 'hdac', 'rbc', 'exact_mass', 'mono_mass', 'tpsa', 'hac', 'charge', 'complex','isc', 'dasc', 'uasc', 'dbsc', 'ubsc', 'cbu']
    #writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    #writer.writeheader()
    #writer.writerow({'Label':Label,'mw': mw, 'xlogp3': xl,'hbdc':hbdc, 'hdac': hdac,'rbc': rbc,'exact_mass':em,'mono_mass': mm,'tpsa': tp,'hac':hac, 'charge':ch,'complex':co,'isc':isc,'dasc':dasc,'uasc':uasc,'dbsc':dbsc,'ubsc':ubsc,'cbu':cbu})
    fieldnames=['Label', 'mw', 'xlogp3', 'hbdc', 'hdac', 'rbc', 'exact_mass', 'mono_mass', 'tpsa', 'hac', 'charge', 'complex','isc', 'dasc', 'uasc', 'dbsc', 'ubsc', 'cbu']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({'Label':Label, 'mw':mw , 'xlogp3':xlogp3, 'hbdc':hbdc , 'hdac': hdac, 'rbc':rbc , 'exact_mass':exact_mass, 'mono_mass': mono_mass , 'tpsa':tpsa , 'hac':hac , 'charge': charge, 'complex': complex  ,'isc': isc , 'dasc': dasc, 'uasc': uasc, 'dbsc': dbsc, 'ubsc': ubsc, 'cbu':cbu})





filename="model_XGB_5_fold_pubchem_1_1"
loaded_model = pickle.load(open(filename, 'rb'))
print (loaded_model)


blindset= pd.read_csv(r'name.csv',sep=',')
Z= blindset.drop('Label',axis=1)
z= blindset['Label']
result = loaded_model.score(Z,z)
#print(result)

