import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import joblib as jl
from code.model import linear_ramp
from code.plotting import parcolors
from scipy.stats import gaussian_kde


def calc_med_iqr(y, q=[5, 95], axis=None):
    qs = np.percentile(y, [q[0], 50, q[-1]], axis=axis)
    yerr = np.diff(qs, axis=0)
    y = qs[1]
    return y, yerr


gi_table = pd.read_table('data/GIS_table.txt', comment='#')

par = 'Ca'
event = 'GI-8c'

ref_age = gi_table.loc[gi_table['Event'] == 'GI-8c', 'Age'].values

data_file = 'data/ramp_data/NGRIP_%s_%s.csv' % (event, par)

t, obs = pd.read_csv(data_file).values.T


t_plot = (ref_age - t) / 1000

traces = jl.load('ramp_fits/traces/NGRIP.gz')
traces = np.array(traces.sel(param=par, event=event))

ramps = np.array([linear_ramp(t, *p) for p in traces[:, :4]])

r_med, r_err = calc_med_iqr(ramps, axis=0)

fig, axes = plt.subplots(nrows=2, ncols=1, sharex=True, sharey=False,
                         gridspec_kw={'height_ratios': [2, 1]},
                         figsize=(3.5, 1.411 * 3.5))
fig.subplots_adjust(hspace=0.0)

axes[0].set_title('Onset of %s' % event)
axes[0].set_ylabel(r'$\ln(\mathrm{%s} \cdot \mathrm{ppb}^{-1})$' % par)
axes[1].set_xlabel('GICC05 Age (kyr before 1950)')
axes[1].set_ylabel('Marg. post. density\n(yr$^{-1}$)')

axes[0].plot(t_plot, obs, color=parcolors[par], lw=0.5)
axes[0].plot(t_plot, r_med, color='k')
axes[0].fill_between(t_plot, r_med - r_err[0], r_med + r_err[1],
                     alpha=.2, color='gray')

time_traces = (traces[:, 0],
               traces[:, 0] + 0.5 * traces[:, 1],
               traces[:, 0] + traces[:, 1])
amp_traces = (traces[:, 2],
              traces[:, 2] + 0.5 * traces[:, 3],
              traces[:, 2] + traces[:, 3])
for yt, tr in zip(amp_traces, time_traces):
    kde = gaussian_kde(tr)
    tr_med = np.median(tr)
    l, = axes[1].plot(t_plot, kde(t), lw=1.0, color='k')
    tmed, terr = calc_med_iqr(tr)
    ymed, yerr = calc_med_iqr(yt)

fig.savefig('figures/fig_02_example_fit.pdf')
