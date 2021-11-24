from pdmpy import pdm
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
import pandas as pd

#paths to data
RVpath = './data22_RV_info.dat'
LCpath = './data22_OGLE.dat'
#read lc data
df_phot = pd.read_csv(LCpath, sep='\s', engine='python')
HJD = np.array(df_phot['HJD'])
I_band = np.array(df_phot['I_band'])
I_Err = np.array(df_phot['I_Err'])

maxtime=HJD[-1]-HJD[0]
mintime = np.min(np.diff(HJD))
print('Maximum time between observations:' +str(maxtime) +' and minimum time: ' +str(mintime) + ' in days.')

# freq, theta = pdm(time, mags, f_min=0.002, f_max=10, delf=1e-3)
freq, theta = pdm(HJD, I_band, I_Err, f_min=2/maxtime, f_max=2/mintime, delf=1e-3)
print(f'      Best Period = {1/freq[np.argmin(theta)]:.8f}', 'd')

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 8))
ax1.plot(HJD, I_band, '.', c='magenta')
ax1.set_xlabel('Time')
ax1.set_ylabel('Mag')
#
ax2.plot(freq, 1-theta, 'magenta')
ax2.set_xlabel('Frequency')
ax2.set_ylabel('1-Theta')
#
ax3.plot(1/freq, 1-theta, 'magenta')
ax3.set(xlabel='Period (days)', ylabel='1-Theta');
plt.xscale('log')

peaks2, _ = find_peaks(1-theta, height=0.04, distance=100)
peri2 = 1/freq[peaks2]
print('Possible periods: ', peri2)
ax2.plot(freq[peaks2], 1-theta[peaks2], "ob")
ax3.plot(1/freq[peaks2], 1-theta[peaks2], "ob")
#
plt.tight_layout()

P1 = 21.906044973#1/freq[np.argmin(theta)]
phase = [ x/P1 % 1 for x in HJD]
df_phot['phase'] = phase
df_phase = df_phot.sort_values('phase', ascending=True).reset_index(drop=True)
fig, ax = plt.subplots(figsize=(6, 4))
plt.plot(df_phase['phase'], df_phase['I_band'], '.', c='magenta', ms=6, label='data')
ax.set(xlabel='Phase', ylabel='Magnitude')
plt.tight_layout()
plt.show()
