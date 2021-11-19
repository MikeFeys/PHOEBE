import phoebe
from phoebe import u
import numpy as np
import matplotlib.pyplot as plt

RVpath = './data22_RV_info.dat'
LCpath = './data22_OGLE.dat'
period_cand = [1,795,663,428,1060] #in days

#read data
HJD=[] # heliocentric julian date
I_band=[] # I-band magnitudes
I_err=[] # error in magnitudes
#read lc data
with open(LCpath) as f:
    for line in f:
        temp=line.split()
        HJD.append(float(temp[0]))
        I_band.append(float(temp[1]))
        I_err.append(float(temp[2]))
for i in range(len(period_cand)):
    b = phoebe.default_binary()

    b.set_value('latex_repr', component='binary', value = 'orb')
    b.set_value('latex_repr', component='primary', value = '1')
    b.set_value('latex_repr', component='secondary', value = '2')
    b.set_value('period@binary', period_cand[i])

    b.add_dataset('lc',
                compute_phases=phoebe.linspace(0,1,201),
                times=HJD,
                fluxes=I_band,
                sigmas = I_err,
                dataset='lc01')

    b.set_value_all('ld_mode','lookup')

    afig, mplfig = b.plot(x='phases',show=False,save='./figs/phased_p'+str(period_cand[i])+'.png')
