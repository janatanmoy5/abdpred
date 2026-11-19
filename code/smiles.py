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

sm= comp.canonical_smiles
print (sm)




