import phoebe
b=phoebe.default_binary()
b.set_value('teff', component='secondary', value=5000)
b.set_value('q', value=0.75)
b.add_dataset('lc', times=phoebe.linspace(0,2,101))
b.add_dataset('rv', times=phoebe.linspace(0,2,101))
b.run_compute()
b.plot(x='phases', show=True)
b.show()
