# Colorcode for figures
from collections import defaultdict

parcolors = defaultdict(lambda: 'black')
parcolors['Ca'] = '#e41a1c'
parcolors['Na'] = '#377eb8'
parcolors['lt'] = '#ff7f00'
parcolors['Ca-Na'] = '#984ea3'
parcolors['lt-Na'] = '#4daf4a'
parcolors['d18O-Na'] = '0.4'

parlabels = {'Ca': 'Ca',
             'Dust': 'Dust',
             'Layerthickness': r'$\lambda$',
             'lt': r'$\lambda$',
             'NH4': 'NH4',
             'Na': 'Na',
             'd18O': '$\delta^{18}\mathrm{O}$'}
