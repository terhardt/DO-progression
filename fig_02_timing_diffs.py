import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import joblib as jl
from matplotlib.patches import ConnectionPatch

plt.style.use('figstyle.mplstyle')


def style_plot(fig, axes):
    fig.subplots_adjust(hspace=0.1)
    for i, ax in enumerate(axes):
        ax.patch.set_alpha(0.0)
        side = ['left', 'right'][i % 2]
        for _, spine in ax.spines.items():
            spine.set_visible(False)
        ax.spines[side].set_visible(True)
        ax.yaxis.set_label_position(side)
        ax.yaxis.set_ticks_position(side)
        ax.xaxis.set_ticks_position('none')
    axes[0].spines['top'].set_visible(True)
    axes[0].xaxis.set_label_position('top')
    axes[-1].spines['bottom'].set_visible(True)
    axes[-1].xaxis.set_ticks_position('bottom')
    axes[0].xaxis.set_ticks_position('top')
    return fig, axes


def vmarker(x0, x1, ax0, ax1, **kwargs):
    xy0 = (x0, ax0.get_ylim()[0])
    xy1 = (x1, ax1.get_ylim()[1])
    ax0.axvline(x0, **kwargs)
    ax1.axvline(x1, **kwargs)
    con = ConnectionPatch(xy0, xy1, 'data', 'data', ax0, ax1, **kwargs)
    ax0.add_artist(con)


def calc_med_iqr(y, q=[5, 95], axis=None):
    qs = np.percentile(y, [q[0], 50, q[-1]], axis=axis)
    yerr = np.diff(qs, axis=0)
    y = qs[1]
    return y, yerr


def calc_point_lags(t0_1, dt_1, t0_2=0, dt_2=0):
    dt0 = t0_1 - t0_2
    dtm = t0_1 + 0.5 * dt_1 - (t0_2 + 0.5 * dt_2)
    dt1 = t0_1 + dt_1 - (t0_2 + dt_2)
    return dt0, dtm, dt1


iso_data = iso_data = pd.read_csv('data/NGRIP_10yr.csv', usecols=(0, 4), comment='#')
iso_data = iso_data.loc[(iso_data['Age_BP'] > 10000) &
                        (iso_data['Age_BP'] <= 60000), :]

gi_table = pd.read_table('data/GIS_table.txt', comment='#')
gi_table = gi_table[['GI' in s or 'Holocene' in s for s in gi_table['Event']]]
gi_table = gi_table[gi_table['Age'] < 60000]
gi_table = gi_table[np.any(gi_table[['NGRIP_Ca', 'NGRIP_Na', 'NGRIP_lt',
                                     'NEEM_Ca', 'NEEM_Na']] == 1.0, axis=1)]
fig, axes = plt.subplots(nrows=4, sharex=False, figsize=(1.414 * 7, 7))

# Isotope data
axes[0].plot(iso_data['Age_BP'] / 1000, iso_data['d18O'], color='k', lw=0.25)

ref_par = 'Na'
x_plt = pd.Series(np.arange(len(gi_table)), gi_table['Event'])

dx = -0.225
# Calcium
for fmt, CORE in zip(('^', 'o'), ['NEEM', 'NGRIP']):
    traces = jl.load('ramp_fits/traces/%s.gz' % CORE) \
        .sel(param=['Ca', ref_par]).dropna(dim='event')
    x = x_plt[np.array(traces.coords['event'])]
    dt0, dtm, dt1 = calc_point_lags(traces.sel(param='Ca', model='t0'),
                                    traces.sel(param='Ca', model='dt'),
                                    traces.sel(param=ref_par, model='t0'),
                                    traces.sel(param=ref_par, model='dt'),)
    for ax, tr in zip(axes[1:], (dt0, dtm, dt1)):
        y, yerr = calc_med_iqr(tr, axis=0)
        ax.errorbar(x + dx, y, yerr, fmt=fmt, ms=2.0, capsize=0,
                    elinewidth=0.75, color='#984ea3',
                    label='Ca$^{2+}$ (%s)' % CORE)
    dx += 0.15

# layer thickness

traces = jl.load('ramp_fits/traces/NGRIP.gz') \
    .sel(param=['lt', ref_par]).dropna(dim='event')
x = x_plt[np.array(traces.coords['event'])]
dt0, dtm, dt1 = calc_point_lags(traces.sel(param='lt', model='t0'),
                                traces.sel(param='lt', model='dt'),
                                traces.sel(param=ref_par, model='t0'),
                                traces.sel(param=ref_par, model='dt'),)
for ax, tr in zip(axes[1:], (dt0, dtm, dt1)):
    y, yerr = calc_med_iqr(tr, axis=0)
    ax.errorbar(x + dx, y, yerr, fmt=fmt, ms=2.0, capsize=0,
                elinewidth=0.75, color='#4daf4a',
                label='$\lambda$ (NGRIP)')
dx += 0.15

traces = jl.load('ramp_fits/traces/NGRIP.gz') \
    .sel(param=['d18O', ref_par]).dropna(dim='event')
x = x_plt[np.array(traces.coords['event'])]
dt0, dtm, dt1 = calc_point_lags(traces.sel(param='d18O', model='t0'),
                                traces.sel(param='d18O', model='dt'),
                                traces.sel(param=ref_par, model='t0'),
                                traces.sel(param=ref_par, model='dt'),)
for ax, tr in zip(axes[1:], (dt0, dtm, dt1)):
    y, yerr = calc_med_iqr(tr, axis=0)
    ax.errorbar(x + dx, y, yerr, fmt=fmt, ms=2.0, capsize=0,
                elinewidth=0.75, color='0.5', label='$\delta^{18}$O (NGRIP)')
dx += 0.15

for i, a in enumerate(gi_table['Age'] / 1000):
    vmarker(a, i, axes[0], axes[1], lw=0.2, ls='solid', zorder=-100)
    vmarker(i, i, axes[1], axes[2], lw=0.2, ls='solid', zorder=-100)
    vmarker(i, i, axes[2], axes[3], lw=0.2, ls='solid', zorder=-100)

for ax in axes[1:]:
    ax.set_xlim(-1.0, len(x_plt))
    ax.axhline(0.0, zorder=-100, lw=0.25, ls='solid')

axes[0].set_ylabel('$\delta^{18}\mathrm{O}$ (‰)')
axes[1].set_ylabel('Onset lag (yr)')
axes[2].set_ylabel('Midpoint lag (yr)')
axes[3].set_ylabel('Endpoint lag (yr)')

axes[0].set_xlabel('GICC05 Age (ka BP)')
axes[0].xaxis.set_major_locator(plt.MultipleLocator(10))
axes[0].xaxis.set_minor_locator(plt.MultipleLocator(2))

axes[-1].set_xlabel('Onset of…')

fig, axes = style_plot(fig, axes)
axes[1].xaxis.set_ticks(())
axes[2].xaxis.set_ticks(())
axes[-1].xaxis.set_ticks(np.arange(len(gi_table)))
axes[-1].xaxis.set_ticklabels(gi_table['Event'],
                              rotation=30, va='top', ha='right')

legend_ax = axes[-1]
legend_ax.legend(loc='lower right', fontsize=5, ncol=4,
                 frameon=True, framealpha=1.0,
                 edgecolor='white', facecolor='white',
                 columnspacing=0.2, borderpad=0.2)

for l, ax in zip(('a', 'b', 'c', 'd'), axes):
    ax.text(0.01, 0.95, l, ha='left', va='top', transform=ax.transAxes,
            weight='bold', fontsize=8)

fig.savefig('figures/fig_02_timing_diffs.pdf')
