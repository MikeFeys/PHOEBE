from astropy.timeseries import LombScargle
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
        HJD.append(float(temp[0]))
        I_band.append(float(temp[1]))
        I_Err.append(float(temp[2]))
#atom-python-run en dan f5
frequencies_Lombscargle = np.linspace(0.01, 100,10000)
frequency, power = LombScargle(HJD, I_band, I_Err).autopower(minimum_frequency=0.1, maximum_frequency=100)
#false alarm levels
probabilities = [0.1,0.05,0.01]
FA_levels = LombScargle(HJD, I_band, I_Err).false_alarm_level(probabilities, method='bootstrap')
plt.plot(frequency, power)
plt.hlines(FA_levels[0],0.1,100,colors = ['red'],linestyle = 'dashed')
plt.hlines(FA_levels[1],0.1,100,colors = ['orange'],linestyle = 'dashed')
plt.hlines(FA_levels[2],0.1,100,colors = ['green'],linestyle = 'dashed')
plt.show()
