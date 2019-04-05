import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import joblib as jl
from code.plotting import parlabels

traces = jl.load('ramp_fits/traces/NGRIP.gz')

nevent = len(traces.coords['event'].values)

order_freq = np.zeros((nevent, 4, 4))

for i, event in enumerate(traces.coords['event'].values):
    t0 = traces.sel(model='t0', event=event)
    t0_order = np.argsort(t0, axis=1)
    f = lambda x: np.bincount(x, minlength=4)
    order_freq[i] = np.array(list(map(f, t0_order.values.T))) / 12000

mean_order = np.mean(order_freq, axis=0)
print(pd.DataFrame(mean_order.T, index=traces.coords['param'].values))

fig, ax = plt.subplots()
img = ax.imshow(mean_order.T, cmap=plt.cm.Blues)
fig.colorbar(img, label='Average probability')
ax.set_xlabel('Order at start of transition')
ax.set_yticks(np.arange(4))
labels = [parlabels[p] for p in traces.coords['param'].values]
ax.set_yticklabels(labels)
ax.set_xticks(np.arange(4))
ax.set_xticklabels(np.arange(4) + 1)

fig.savefig('figures/fig_05_order.pdf')
