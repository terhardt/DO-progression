import numpy as np
import matplotlib.pyplot as plt
import joblib as jl
from code.plotting import parcolors, parlabels


traces = jl.load('ramp_fits/traces/NGRIP.gz')

uncert = traces.sel(model='t0').std(axis=0)
snr = np.abs((traces.sel(model='dy')
             / traces.sel(model='sigma')).mean(dim='sample'))


lags = (traces.sel(model='t0', param=['Ca', 'lt', 'd18O'])
        - traces.sel(model='t0', param='Na')).mean(dim='sample')


fig, ax = plt.subplots()
for param in lags.coords['param'].values:
    x, y = snr.sel(param=param).values, lags.sel(param=param).values
    l, = ax.plot(snr.sel(param=param), lags.sel(param=param), '.',
                 label=parlabels[param],
                 color=parcolors['%s-Na' % param])
ax.set_ylabel('Lag of $t_0$ relative to Na (yr)')
ax.set_xlabel(r'SNR $\left(\mid\Delta y / \sigma\mid\right)$')
ax.legend()
ax.axhline(0, ls='--')
ax.set_ylim(-65, 65)

fig.savefig('figures/fig_S02_SNR_lag_NGRIP.pdf')
