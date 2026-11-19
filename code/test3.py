import pubchempy as pcp
from array import *
from pubchempy import Compound
import pandas as pd
#import php
import sys
import os
import pandas as pd
import numpy as np



inpv = int(sys.argv[1])
a=inpv
inpv1 = int(sys.argv[2])


filename = (str(inpv1)+'syno.txt')

comp= Compound.from_cid(a)

if comp!=0:
    names=comp.synonyms
    print (names)
    f = open(filename, "a")
    f.write(str(names))
    f.close()
else:
  print("Please check internet connection")

