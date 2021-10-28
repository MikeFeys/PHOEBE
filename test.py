from astropy.timeseries import LombScargle
import numpy as np
import matplotlib.pyplot as plt
#paths to data
RVpath = './data22_RV_info.dat'
LCpath = './data22_OGLE.dat'
# initialize data arrays
HJD=[] # heliocentric julian date
I_band=[] # I-band
I_Err=[] # error in magnitudes
#read lc data
with open(LCpath) as f:
    for line in f:
        temp=line.split()
        HJD.append(float(temp[0]))
        I_band.append(float(temp[1]))
        I_Err.append(float(temp[2]))
#plot raw lc data
fig0 = plt.figure()
ax0 = plt.gca()
ax0.errorbar(HJD, I_band, I_Err, fmt='o')
plt.show()
#maximum and minimum time differences for Nyquist frequency
maxtime=HJD[-1]-HJD[0]
mintime = np.min(np.diff(HJD))
# make lombscargle periodogram
frequency, power = LombScargle(HJD, I_band, I_Err).autopower(samples_per_peak=100,minimum_frequency=2/(maxtime), maximum_frequency=2/mintime)
#false alarm levels
probabilities = [0.1,0.05,0.01]
FA_levels = LombScargle(HJD, I_band, I_Err).false_alarm_level(probabilities, method='bootstrap')
#plot lombscargle periodogram
plt.plot(1/frequency, power)
plt.hlines(FA_levels[0], maxtime/2,mintime/2,colors = ['red'],linestyle = 'dashed')
plt.hlines(FA_levels[1],maxtime/2,mintime/2,colors = ['orange'],linestyle = 'dashed')
plt.hlines(FA_levels[2],maxtime/2,mintime/2,colors = ['green'],linestyle = 'dashed')
plt.show()
#extract the period associated to the absolute maximum in power
max=np.max(power)
index=np.where(power == max)[0][0]
period = frequency[index]
print(period)
print(frequency[np.where(power== np.amax(power))])
