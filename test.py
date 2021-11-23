from astropy.timeseries import LombScargle
import numpy as np
import matplotlib.pyplot as plt
#paths to data
RVpath = './data22_RV_info.dat'
LCpath = './data22_OGLE.dat'
# initialize data arrays
HJD=[] # heliocentric julian date
I_band=[] # I-band magnitudes
I_Err=[] # error in magnitudes
#read lc data
with open(LCpath) as f:
    for line in f:
        temp=line.split()
        HJD.append(np.float(temp[0]))
        I_band.append(np.float(temp[1]))
        I_Err.append(np.float(temp[2]))
'''
#conversion mag to flux: Magnitude = 22.5 - 2.5log_10(flux) so flux=10**((Magnitude-22.5)/-2.5)
I_flux = np.divide((I_band-np.ones(len(I_band))*22.5),-2.5)
I_flux_err = (I_Err-np.ones(len(I_band))*22.5)/-2.5
'''
#plot raw lc data
fig0 = plt.figure()
ax0 = plt.gca()
ax0.errorbar(HJD, I_band, I_Err, fmt='o')
plt.xlabel('HJD [d]')
plt.ylabel('I band magnetude')
plt.title('Light curve data of I band vs heliocentric julian date')
'''
fig1 = plt.figure()
ax1 = plt.gca()
ax1.errorbar(HJD, I_flux, I_flux_err, fmt='o')
plt.xlabel('HJD [d]')
plt.ylabel('I band Flux')
plt.title('Flux of I band vs heliocentric julian date')
'''
#maximum and minimum time differences for Nyquist frequency
maxtime=HJD[-1]-HJD[0]
mintime = np.min(np.diff(HJD))
# make lombscargle periodogram
frequency, power = LombScargle(HJD, I_band, I_Err).autopower(samples_per_peak=100,minimum_frequency=2/(maxtime), maximum_frequency=2/mintime)
#false alarm levels
probabilities = [0.1,0.05,0.01]
FA_levels = LombScargle(HJD, I_band, I_Err).false_alarm_level(probabilities, method='bootstrap')
#look for best frequencies
bestfreq = []
bestind = []
search_freq = frequency
search_pow = power
for i in range(5):
    bestind = np.argmax(search_pow)
    bestfreq = search_freq[bestind]
    search_freq = np.delete(search_freq,bestind)
    search_pow = np.delete(search_pow,bestind)
print(bestfreq)
#plot lombscargle periodogram
plt.figure()
plt.plot(1/frequency, power)
plt.hlines(FA_levels[0], maxtime/2,mintime/2,colors = ['red'],linestyle = 'dashed')
plt.hlines(FA_levels[1],maxtime/2,mintime/2,colors = ['orange'],linestyle = 'dashed')
plt.hlines(FA_levels[2],maxtime/2,mintime/2,colors = ['green'],linestyle = 'dashed')
plt.text(maxtime/2,0.95*FA_levels[0],'10%',color='red')
plt.text(maxtime/2,FA_levels[1],'5%',color='orange')
plt.text(maxtime/2,FA_levels[2],'1%',color='green')
plt.xlabel('Period [days]')
plt.ylabel('Power [no unit/normalized]')
plt.title('Lombscargle periodogram using bootstrap method for false alarms.')
plt.show()
#extract the frequency associated to the absolute maximum in power
print(frequency[np.where(power== np.amax(power))])
