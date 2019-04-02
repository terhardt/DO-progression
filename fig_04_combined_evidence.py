import numpy as np
import matplotlib.pyplot as plt
import joblib as jl
from code.plotting import parcolors
from code.combined_kde import combined_kde

plt.style.use('figstyle.mplstyle')


def calc_med_iqr(y, q=[5, 95], axis=None):
    qs = np.percentile(y, [q[0], 50, q[-1]], axis=axis)
    yerr = np.diff(qs, axis=0)
    y = qs[1]
    return y, yerr


def format_qs(qs):
    template = '{:.0f} (+{:.0f}/-{:.0f})'
    return template.format(qs[1], qs[2] - qs[1], qs[1] - qs[0])


cores = ['NGRIP', 'NEEM']
params = ['Ca', 'lt', 'd18O']
ref_par = 'Na'

print('Initiating KDEs')

kdes = dict()
for CORE in cores:
    kdes[CORE] = dict()
    traces = jl.load('ramp_fits/traces/%s.gz' % CORE)
    for p in params:
        if not np.any(np.isfinite(traces.sel(param=p))):
            continue
        t0_tr = np.diff(traces.sel(param=[ref_par, p], model='t0')
                        .dropna(dim='event'), axis=1).squeeze()
        tm_tr = np.diff(traces.sel(param=[ref_par, p], model='t0')
                        .dropna(dim='event') +
                        0.5 * traces.sel(param=[ref_par, p], model='dt')
                        .dropna(dim='event'), axis=1).squeeze()
        t1_tr = np.diff(traces.sel(param=[ref_par, p], model='t0')
                        .dropna(dim='event') +
                        traces.sel(param=[ref_par, p], model='dt')
                        .dropna(dim='event'), axis=1).squeeze()
        kdes[CORE][p] = [combined_kde(t0_tr.T),
                         combined_kde(tm_tr.T),
                         combined_kde(t1_tr.T)]


# print timing difference estimates
# these are used in the paper
for ls, CORE in zip(['solid', 'dashed'], cores):
    print(CORE)
    for p in params:
        if p not in kdes[CORE]:
            continue
        print()
        for l, kde in zip(('t0', 'tm', 't1'), kdes[CORE][p]):
            print(p, l, format_qs(-1 * kde.ppf((0.95, 0.5, 0.05))))


fig, axes = plt.subplots(ncols=3, sharex=True, sharey=True,
        figsize=(7, 7 / (2.5 * 1.414)))
(t0_ax, tm_ax, t1_ax) = axes
fig.subplots_adjust(wspace=0.05)
x = np.linspace(-25, 25, 500)

for ls, CORE in zip(['solid', 'dashed'], cores):
    for p in params:
        if p not in kdes[CORE]:
            continue
        for kde, ax in zip(kdes[CORE][p], axes):
            ax.plot(x, kde.pdf(x), color=parcolors['%s-%s' % (p, ref_par)],
                    ls=ls, lw=1.0)

for l, ax in zip(['a', 'b', 'c'], axes):
    ax.text(0.05, 0.95, l, ha='left', va='top',
            transform=ax.transAxes, weight='bold', size=10)

for point, ax in zip(('onset', 'midpoint', 'endpoint'), axes):
    ax.set_xlabel('Lag to %s$^{+}$ at %s (yr)' % (ref_par, point))


legend_ax = axes[2]
legend_ax.plot((), (), color=parcolors['Ca-Na'],
               ls='solid', label='Ca$^{2+}$ (NGRIP)', lw=1.0)
legend_ax.plot((), (), color=parcolors['Ca-Na'],
               ls='dashed', label='Ca$^{2+}$ (NEEM)', lw=1.0)
legend_ax.plot((), (), color=parcolors['lt-Na'],
               ls='solid', label='$\lambda$ (NGRIP)', lw=1.0)
legend_ax.plot((), (), color=parcolors['d18O-Na'],
               ls='solid', label='$\delta^{18}$O (NGRIP)', lw=1.0)
legend_ax.legend(loc='upper right', fontsize=7)

for ax in axes:
    [ax.spines[s].set_visible(False) for s in ax.spines]
    ax.spines['bottom'].set_visible(True)
    ax.yaxis.set_ticks_position('none')
axes[0].set_ylabel('Probability density (yr$^{-1}$)')
axes[0].spines['left'].set_visible(True)
axes[0].yaxis.set_ticks_position('left')

fig.savefig('figures/fig_04_combined_evidence.pdf')
