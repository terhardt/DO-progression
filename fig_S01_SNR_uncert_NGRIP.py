import numpy as np
import matplotlib.pyplot as plt
import joblib as jl
from code.plotting import parcolors, parlabels


traces = jl.load('ramp_fits/traces/NGRIP.gz')

uncert = traces.sel(model='t0').std(axis=0)
snr = np.abs((traces.sel(model='dy')
             / traces.sel(model='sigma')).mean(dim='sample'))

fig, ax = plt.subplots()

for param in snr.coords['param'].values:
    x, y = snr.sel(param=param).values, uncert.sel(param=param).values
    l, = ax.plot(snr.sel(param=param), uncert.sel(param=param), '.',
                 label=parlabels[param],
                 color=parcolors[param])
    fit = np.polyfit(x[np.isfinite(x)], y[np.isfinite(x)], 1)
    x_plt = np.sort(x[np.isfinite(x)])
    ax.plot(x_plt, np.polyval(fit, x_plt), color=l.get_color(), ls='dashed')
ax.set_xlabel(r'SNR $\left(\mid\Delta y / \sigma\mid\right)$')
ax.set_ylabel('Marg. post. SD of $t_0$ (yr)')
ax.legend()

fig.savefig('figures/fig_S01_SNR_uncert_NGRIP.pdf')
