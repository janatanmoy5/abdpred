import numpy as np
import pubchempy as pcp
from array import *
from pubchempy import Compound
import pandas as pd
import sys
import os



currUID = int(sys.argv[1])
#print ("You have entered CID value: ",currUID)

directory=currUID
#print(directory)


filename2 = (str(directory)+'check_id.csv')


#file1 = open('myfile.txt', 'w')

dataset = pd.read_csv(filename2,sep=',')
Label=0
#print (dataset.values)
print ("Label, mw, xlogp3, hbdc, hdac, rbc, exact_mass, mono_mass, tpsa, hac, charge, complex,isc, dasc, uasc, dbsc, ubsc, cbu")
#den = array([dataset.values])

#file = (str(directory)+'cid.txt')

for x in dataset.values:
    #f = open(file, "a")
    #f.write(str(x))
    #f.write("\n")
    #f.close()
    #print (x)
    comp= Compound.from_cid(x)
    #print(comp)
    mw= comp.molecular_weight
    xl= comp.xlogp
    hbdc= comp.h_bond_donor_count
    hdac= comp.h_bond_acceptor_count 
    rbc= comp.rotatable_bond_count 
    em= comp.exact_mass
    mm= comp.monoisotopic_mass 
    tp= comp.tpsa
    hac= comp.heavy_atom_count 
    ch= comp.charge
    co= comp.complexity 
    isc= comp.isotope_atom_count 
    dasc= comp.defined_atom_stereo_count 
    uasc= comp.undefined_atom_stereo_count 
    dbsc= comp.defined_bond_stereo_count
    ubsc= comp.undefined_bond_stereo_count 
    cbu= comp.covalent_unit_count
    #out= mw,",", xl, ",", hbdc,",", hdac,",", rbc, ",", em,",", mm, ",", tp,",", hac, ",", ch, ",", co, ",",isc, ",", dasc, ",",uasc,",",dbsc,",",ubsc,",",cbu 
    #print (out)
    
    print(Label,",",mw,",", xl, ",", hbdc,",", hdac,",", rbc, ",", em,",", mm, ",", tp,",", hac, ",", ch, ",", co, ",",isc, ",", dasc, ",",uasc,",",dbsc,",",ubsc,",",cbu)
    #out= mw,",", xl, ",", hbdc,",", hdac,",", rbc, ",", em,",", mm, ",", tp,",", hac, ",", ch, ",", co, ",",isc, ",", dasc, ",",uasc,",",dbsc,",",ubsc,",",cbu 
    #np.savetxt('file.txt', zip(out[]), fmt="%5.2f")
    #df = pd.DataFrame(data=out.append)
    #df.to_csv('data1.csv')
    





  

