import pubchempy as pcp
from array import *
from pubchempy import Compound
import pandas as pd
#import php
import sys
import os
import pandas as pd
import numpy as np

currUID = int(sys.argv[1])
#print ("You have entered CID value: ",currUID)

a=currUID
comp= Compound.from_cid(a)
Label=0

#sm= comp.canonical_smiles
#print (sm)


a=currUID
comp= Compound.from_cid(a)

mw= comp.molecular_weight
xlogp3= comp.xlogp
hbdc= comp.h_bond_donor_count
hdac= comp.h_bond_acceptor_count 
tpsa= comp.tpsa
rbc= comp.rotatable_bond_count 

#print (mw)
#print (hdac)
#print (hbdc)
#print (xlogp3)
#print (tpsa)
#print (rbc)
#Lipinski's rule
if mw < 500 and  hbdc<= 5 and hdac <=10 and xlogp3<=5:
	print("Follows")
else:
    print ("Does not follow")
    
# Pfizer 3/75   
if xlogp3 >=3 and tpsa <=75:
	print("Follows")
else:
    print ("Does not follow")
#veber's rule

if tpsa >=140 and rbc >=10:
    print("Follows")
else:
    print ("Does not follow")
    
#Egan's Rule  
  
if tpsa >=131.6 and xlogp3 >=5.88:
    print("Follows")
else:
    print ("Does not follow")

