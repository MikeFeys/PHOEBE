import phoebe
import pandas as pd
import numpy as np
from phoebe import u
import matplotlib.pyplot as plt

# best period
P = 21.906044973
e = 0.38799870437066447
#rv properties in km/s
K1 = 69.7
K1err = 1.3
K2 = 137
K2err = 34

q = K1/K2

# estimate asini in case of e=0
a1sini = np.sqrt(1-e**2)/(2*np.pi)*K1*P*86400/695700
a2sini = np.sqrt(1-e**2)/(2*np.pi)*K2*P*86400/695700

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

# convert mag to flux

def to_flux(mag_array,errs,boolean):
    flux_array=[]
    flux_arrayerr1=[]
    flux_arrayerr2=[]
    if boolean:
        for i,j in zip(mag_array,errs):
            flux_arrayerr1.append(np.power(10,-((i-j)-15.275)/2.5)) #use mean of fluxes for zero point when converting, eclipse will be down now
            flux_arrayerr2.append(np.power(10,-((i+j)-15.275)/2.5))
        flux_array=[(a-b)/2 for a,b in zip(flux_arrayerr1,flux_arrayerr2)]
    else:
        for i in mag_array:
            flux_array.append(np.power(10,-(i-15.275)/2.5)) #use mean of fluxes for zero point when converting, eclipse will be down now
    return flux_array

flux = to_flux(mag,err,False)
err = to_flux(mag,err,True)


#init logger and binary package

logger = phoebe.logger(clevel='WARNING')

b = phoebe.default_binary()

#add lc dataset

b.add_dataset('lc', times=time,
                    fluxes=flux,
                    sigmas=err,
                    dataset='lc01')


#alter settings
b.set_value_all('atm', 'blackbody')
b.set_value_all('ld_mode', 'manual')
b.set_value_all('ld_mode_bol', 'manual')



b.set_value('latex_repr', component='binary', value = 'orb')
b.set_value('latex_repr', component='primary', value = '1')
b.set_value('latex_repr', component='secondary', value = '2')

b.set_value(qualifier='compute_times', dataset='lc01', context='dataset', value=np.linspace(time[0], time[-1], 200))
#b.set_value('teff', component='primary', value=50000)
#b.set_value('teff', component='secondary', value=29000)
#b.set_value('gravb_bol', component='primary', value=0.9)
#b.set_value('gravb_bol', component='secondary', value=0.9)
#b.set_value('irrad_frac_refl_bol', component='primary', value=1)
#b.set_value('irrad_frac_refl_bol', component='secondary', value=1)
b.set_value(qualifier='period', component = 'binary', context='component', value= P )
b.set_value(qualifier='q', component = 'binary', context='component', value= q )
b.flip_constraint('asini@binary', solve_for='sma@binary')
b.set_value(qualifier='asini', component='binary', context='component', value=asini)
b.set_value(qualifier='q', component='binary', context='component', value=69.7/137)
b.set_value(qualifier='incl', component = 'binary', context='component', value= 90 )

'''
# plot flux data
afig, mplfig = b.plot(x='phases', m='.', show=True)
plt.close()
'''
print(b.filter(context='component'))

# run model
b.set_value('pblum_mode', dataset='lc01' , context='dataset',value='dataset-scaled')
b.run_compute(model='default')

_ = b.plot(x='phases', m='.', show=True)


# add estimator
#lcgeom
b.add_solver('estimator.lc_geometry', solver='lcgeom')
b.run_solver('lcgeom', solution='lcgeom_solution')

print(b.adopt_solution('lcgeom_solution'))

#recompute with lc_geom
b.run_compute(model='lcgeom_model')
_ = b.plot(x='phases', ls='-', m='.', legend=True, show=True)

print(b.filter(context='component'))
print(b.get_parameter(qualifier='mass', component='primary', context='component'))
print(b.get_parameter(qualifier='sma', component='binary', context='component'))

'''
#add optimizer
b.add_solver('optimizer.nelder_mead', solver='nm_solver')
b.set_value('compute', solver='nm_solver', value='phoebe01')
b.set_value('maxiter', 100)
b.set_value('maxfev', 1000)

b.set_value('fit_parameters', ['q', 'ecc'])

b.run_solver('nm_solver', solution='nm_sol')

print(b.filter(solution='nm_sol'))
print(b.adopt_solution(trial_run=True))
'''
