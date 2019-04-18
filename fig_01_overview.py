"""Script to produce Figure 1

This Figure shows the overview of the data used in the study
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


plt.style.use('figstyle.mplstyle')


def move_axes(ax, dx=0.0, dy=0.0):
    bbox = ax.get_position()
    bbox.y0 = bbox.y0 + dy
    bbox.y1 = bbox.y1 + dy
    bbox.x0 = bbox.x0 + dx
    bbox.x1 = bbox.x1 + dx
    ax.set_position(bbox)
    return ax


def style_plot(fig, axes):
    fig.subplots_adjust(hspace=0.0)
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
    axes[-1].spines['bottom'].set_visible(True)
    axes[-1].xaxis.set_ticks_position('bottom')
    axes[0].xaxis.set_ticks_position('top')
    return axes


NGRIP_data = pd.read_csv('data/NGRIP_10yr.csv', comment='#')
NEEM_data = pd.read_csv('data/NEEM_10yr.csv', comment='#')

gi_table = pd.read_table('data/GIS_table.txt', comment='#')
gi_table = gi_table[['GI' in s or 'Holocene' in s for s in gi_table['Event']]]
gi_table = gi_table[gi_table['Age'] < 60000]
gi_table = gi_table[np.any(gi_table[['NGRIP_Ca', 'NGRIP_Na', 'NGRIP_lt',
                                     'NEEM_Ca', 'NEEM_Na']] == 1.0, axis=1)]


fig, axes = plt.subplots(nrows=6, sharex=True, figsize=(1.414 * 7, 7))

l, = axes[2].plot(NGRIP_data['Age_BP'] / 1000, NGRIP_data['Ca'], color='#e41a1c', lw=0.25)
axes[2].set_yscale('log')
axes[2].set_ylabel('NGRIP\nCa$^{2+}$ (ppb)', color=l.get_color())


l, = axes[0].plot(NEEM_data['Age_BP'] / 1000, NEEM_data['Ca'], color='#e41a1c', lw=0.25)
axes[0].set_yscale('log')
axes[0].set_ylabel('NEEM\nCa$^{2+}$ (ppb)', color=l.get_color())


l, = axes[3].plot(NGRIP_data['Age_BP'] / 1000, NGRIP_data['Na'], color='#377eb8', lw=0.25)
axes[3].set_yscale('log')
axes[3].set_ylabel('NGRIP\nNa$^{+}$ (ppb)', color=l.get_color())

l, = axes[1].plot(NEEM_data['Age_BP'] / 1000, NEEM_data['Na'], color='#377eb8', lw=0.25)
axes[1].set_yscale('log')
axes[1].set_ylabel('NEEM\nNa$^{+}$ (ppb)', color=l.get_color())


l, = axes[4].plot(NGRIP_data['Age_BP'] / 1000, NGRIP_data['lt'] * 1000,
                  color='#ff7f00', lw=0.25)
axes[4].set_yscale('log')
axes[4].set_ylabel('NGRIP\n$\lambda$ (mm)', color=l.get_color())

l, = axes[5].plot(NGRIP_data['Age_BP'] / 1000, NGRIP_data['d18O'],
                  color='black', lw=0.25)
axes[5].set_ylabel('NGRIP\n$\delta^{18}\mathrm{O}$ (\u2030)', color=l.get_color())

axes = style_plot(fig, axes)
move_axes(axes[1], dy=0.05)

move_axes(axes[2], dy=0.05)
move_axes(axes[3], dy=0.1)

move_axes(axes[4], dy=0.10)
move_axes(axes[5], dy=0.10)



axes[-1].set_xlabel('GICC05 Age (kyr before 1950)')
axes[-1].xaxis.set_major_locator(plt.MultipleLocator(5))
axes[-1].xaxis.set_minor_locator(plt.MultipleLocator(1))


for ax in axes:
    for a in gi_table['Age']:
        ax.axvline(a / 1000, lw=0.5, zorder=-100, ls='solid')
    ax.set_xlim(8.000, 62.000)

for l, x, ax in zip(('a', 'b', 'c', 'd', 'e', 'f'), (0.01, 0.97, 0.01, 0.97, 0.01, 0.97), axes):
    ax.text(x, 0.95, '(%s)' % l, ha='left', va='top', transform=ax.transAxes,
            weight='bold', fontsize=7)

fig.savefig('figures/fig_01_overview.pdf')
