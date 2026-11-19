import pubchempy as pcp
from array import *
from pubchempy import Compound
import pandas as pd
import php
import sys
import os
import pandas as pd
import numpy as np

currUID = int(sys.argv[1])
#print ("You have entered CID value: ",currUID)

a=currUID
comp= Compound.from_cid(a)
Label=0
mw= comp.molecular_weight

xlogp3= comp.xlogp
if xlogp3==None:
    xlogp3=1.125
else:
    xlogp3=xlogp3
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
print ("Label, mw, xlogp3, hbdc, hdac, rbc, exact_mass, mono_mass, tpsa, hac, charge, complex,isc, dasc, uasc, dbsc, ubsc, cbu")
print(Label,",", mw,",", xlogp3, ",", hbdc,",", hdac,",", rbc, ",", exact_mass,",", mono_mass, ",", tpsa,",", hac, ",", charge, ",", complex, ",",isc, ",", dasc, ",",uasc,",",dbsc,",",ubsc,",",cbu)
#descriptor=mw,xl,hbdc,hdac,rbc,em,mm,tp,hac,ch,co,isc,dasc,uasc,dbsc,ubsc,cbu    
#print (complex)
