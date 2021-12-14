import phoebe
from phoebe import u
import numpy as np
import matplotlib.pyplot as plt
import warnings
import sys
#Suppress annoying warnings
if not sys.warnoptions:
    warnings.simplefilter("ignore")
RVpath = './data22_RV_info.dat'
LCpath = './data22_OGLE.dat'
period_cand = [21.90611124037] #in days

def to_flux(mag_array):
    flux_array = np.power(10*np.ones(len(mag_array)),-(mag_array-15.275)/2.5) #use mean of fluxes for zero point when converting, eclipse will be down now
    return flux_array

#read data
HJD=[] # heliocentric julian date
I_band=[] # I-band magnitudes
I_err=[] # error in magnitudes
#read lc data
with open(LCpath) as f:
    for line in f:
        if 'HJD' in line:
            pass
        else:
            temp=line.split()
            HJD.append(float(temp[0]))
            I_band.append(float(temp[1]))
            I_err.append(float(temp[2]))


#I_band = to_flux(np.array(I_band))
#I_err = to_flux(np.array(I_err))
#I_err = np.zeros(len(I_band))
#Get min mass companion from binary mass function, https://astronomy.swin.edu.au/cosmos/b/Binary+Mass+Function
fm1m2=(21.90611124037*86400*(69.7e3)**3 /(2* np.pi * 6.67e-11*1.9891e30))
rv=137/69.7
m2=(1+rv)*fm1m2
m1=rv*m2
print('Mass1=',m1, '\n'+'Mass2=',m2)
saving = False

for i in range(len(period_cand)):
    b = phoebe.default_binary()

    b.set_value('latex_repr', component='binary', value = 'orb')
    b.set_value('latex_repr', component='primary', value = '1')
    b.set_value('latex_repr', component='secondary', value = '2')
    b.set_value('period@binary', period_cand[i]*u.d)

    b.add_dataset('lc',
                compute_phases=phoebe.linspace(0,1,201),
                times=HJD,
                fluxes=I_band,
                sigmas = I_err,
                dataset='lc01')
    b.set_value_all('ld_mode','lookup')
    #From the jupyter demonstration,
    #How to estimate M1 mass ???
    print(b.filter(dataset='lc01').contexts)
    print(b.filter(context='component'))
    b.add_solver('estimator.lc_geometry',solver='lcgeom', overwrite=True)
    print(b.filter(solver='lcgeom'))
    b.run_solver('lcgeom', solution='lcgeom_solution')
    print(b.filter(solution='lcgeom_solution'))
    if saving == True:
        afig, mplfig = b.plot(x='phases',show=False,save='./figs/phased_p'+str(period_cand[i])+'.png')
    else:
        afig, mplfig = b.plot(x='phases',show=True)
