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
                fluxes=to_flux(I_band,I_err,False),
                sigmas = to_flux(I_band,I_err,True),
                dataset='lc01')
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
