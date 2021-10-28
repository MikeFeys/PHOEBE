import scipy.signal as signal
import numpy as np
import matplotlib.pyplot as plt

RVpath = './data22_RV_info.dat'
LCpath = './data22_OGLE.dat'

HJD=[]
I_band=[]
I_Err=[]
with open(LCpath) as f:
    for line in f:
        temp=line.split()
        HJD.append(temp[0])
        I_band.append(temp[1])
        I_Err.append(temp[2])
print(I_band)
#atom-python-run en dan f5
frequencies_Lombscargle = np.linspace(0.01, 100,10000)
