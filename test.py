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
        HJD.append(float(temp[0]))
        I_band.append(float(temp[1]))
        I_Err.append(float(temp[2]))

#conversion mag to flux: Magnitude = 22.5 - 2.5log_10(flux) so flux=10**((Magnitude-22.5)/-2.5)

if True:
    #plot raw lc data
    fig0 = plt.figure()
    ax0 = plt.gca()
    ax0.errorbar(HJD, I_band, I_Err, fmt='o',c='blue',markeredgecolor='gray',
             markerfacecolor='black',
             Linestyle='None',markersize=4)
    plt.xlabel('HJD [d]')
    plt.ylabel('I band magnetude')
    plt.title('Light curve data of I band vs heliocentric julian date')
if True:
    #maximum and minimum time differences for Nyquist frequency
    maxtime=HJD[-1]-HJD[0]
    mintime = np.min(np.diff(HJD))
    # make lombscargle periodogram
    frequency, power = LombScargle(HJD, I_band, I_Err).autopower(samples_per_peak=100,minimum_frequency=2/(maxtime), maximum_frequency=2/mintime,method='cython')
    #false alarm levels
    probabilities = [0.1,0.05,0.01]
    FA_levels = LombScargle(HJD, I_band, I_Err).false_alarm_level(probabilities, method='bootstrap')
    #plot lombscargle periodogram
if True:
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
#extract the frequency associated to the absolute maximum in power
#list_1percent_period=[1/frequency[np.where(power==i)] for i in power if i>=FA_levels[2]] #Dit werkt niet omdat er te veel punten zijn, alleen de pieken van de bergen zijn nodig
#print(list_1percent_period)
print('The periods above 1% are ', str(1/frequency[np.where(power== np.amax(power))]))
plt.show()
