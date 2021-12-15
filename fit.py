import phoebe
import pandas as pd
import numpy as np
from phoebe import u
import matplotlib.pyplot as plt

# best period
P = 21.906044973

#rv properties in km/s
K1 = 69.7
K1err = 1.3
K2 = 137
K2err = 34

# estimate asini in case of e=0
a1sini = 1/(2*np.pi)*K1*P
a2sini = 1/(2*np.pi)*K2*P

asini = a1sini + a2sini

#read lc data

datafile = "data22_OGLE.dat"

df_lc = pd.read_csv(datafile, sep='\s', engine='python')

time = np.array(df_lc['HJD'])
mag = np.array(df_lc['I_band'])
maxmag = np.max(mag)
err = np.array(df_lc['I_err'])

#plot obs distribution

'''
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 6))

ax1.plot(time, mag, 'b.', ms=12, mfc='none', alpha=0.5)
ax1.set(ylabel='Magnitude')
ax2.set(ylabel='Magnitude')
ax2.set(xlabel='JD (d)')
ax2.plot(time, mag, 'b.', ms=12, mfc='none', alpha=0.5)
plt.suptitle('Length of observations = '+ '{0:.2f}'.format(time[-1]-time[0])+' d', fontsize=28)
plt.tight_layout()
plt.show()
plt.close()
'''
# convert mag to flux [this is possibly still wrong]

def to_flux(mag_array):
    flux_array = np.power(10*np.ones(len(mag_array)),(-22.614 - mag_array/2.5))
    return flux_array


print(max(mag))
print(max(err))
flux = to_flux(mag)
err = to_flux(err)
print(max(flux))
print(max(err))

#init logger and binary package

logger = phoebe.logger(clevel='WARNING')

b = phoebe.default_binary()

#add lc dataset

b.add_dataset('lc', times=time,
                    fluxes=flux,
                    sigmas=err,
                    dataset='lc01')

#b.set_value('pblum-mode', value='dataset-scaled')
b.set_value(qualifier='compute_times', dataset='lc01', context='dataset', value=np.linspace(time[0], time[-1], 200))
b.set_value(qualifier='period', component = 'binary', context='component', value= P )
b.flip_constraint('asini@binary', solve_for='sma@binary')
b.set_value(qualifier='asini', component='binary', context='component', value=asini)

# plot model
afig, mplfig = b.plot(x='phases', show=True)

# run model
b.run_compute()
