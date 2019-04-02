"""Script to generate supplementary data files"""
import numpy as np
import pandas as pd
import joblib as jl

timing_header = '''# Supplementary data file for: Decadal-scale progression of Dansgaard-Oeschger warming events, by Erhardt et al.
#
# Timing of the transitions in all parameters relative to the ages (in yrs BP, years before 1950) of the GS/GI transitions provided by Rasmussen et al. (2014).
# All values are given as the marignal posterior 50th, 5th and 95th percentile in years.
# Note that the CI for the transition points are with respect to the age stated in the Age column but do not include the uncertainty of that age as given by the maximum counting error (MCE).
#
# For details on the data and methods please refer to the main manuscript and supplementary material
#
'''

lags_header = '''# Supplementary data file for: Decadal-scale progression of Dansgaard-Oeschger warming events, by Erhardt et al.
#
# Lags relative to the transition points in Na for each of the investigated transitions.
# All values are give as the marginal posterior 50th, 5th and 95th percentile in years
# Note that the differences of two parameters with respect to Na cannot necessarily be used to infer the timing difference between the two parameters themselves due to the correlation of the uncertainties in their lags.
# This correlation arises from the uncertainty of the timing in the reference parameter.
#
# For details on the data and methods please refer to the main manuscipt and supplementary material
#
'''

with open('results/NGRIP_timing.csv', 'w') as f:
    f.write(timing_header)

with open('results/NEEM_timing.csv', 'w') as f:
    f.write(timing_header)

with open('results/NGRIP_lags.csv', 'w') as f:
    f.write(lags_header)

with open('results/NEEM_lags.csv', 'w') as f:
    f.write(lags_header)

gi_table = pd.read_table('data/GIS_table.txt', comment='#', index_col=0)
gi_table['Age'] -= 50.0  # convert b2k to before 1950 ages

cols = pd.MultiIndex.from_product((['Age', 'MCE'], [''], ['']),
                                  names=['par', 'point', 'quantile'])
ages = pd.DataFrame(index=gi_table.index,
                    columns=cols, data=gi_table[['Age', 'MCE']].values)


# NGRIP timing results
pars = ['Na', 'Ca', 'lt', 'd18O']
points = ['start', 'mid', 'end', 'length']
quantiles = np.array([50, 5, 95])

columns = pd.MultiIndex.from_product((pars, points, quantiles),
                                     names=['par', 'point', 'quantile'])
out = pd.DataFrame(index=gi_table.index, columns=columns, dtype=np.float)


traces = jl.load('ramp_fits/traces/NGRIP.gz').sel(param=pars)
start_tr = traces.sel(model='t0')
len_tr = traces.sel(model='dt')
end_tr = start_tr + len_tr
mid_tr = start_tr + 0.5 * len_tr

for tr, point in zip((start_tr, mid_tr, end_tr, len_tr),
                     ('start', 'mid', 'end', 'length')):
    for i in range(len(pars)):
        perc = np.percentile(tr[:, i, :], quantiles, axis=0)
        out.loc[:, (pars[i], point)] = perc.T

pd.concat((ages, out), axis=1).to_csv('results/NGRIP_timing.csv',
                                      float_format='%.1f', mode='a')
del out


# NEEM timing results
pars = ['Na', 'Ca']
points = ['start', 'mid', 'end', 'length']
quantiles = np.array([50, 5, 95])

columns = pd.MultiIndex.from_product((pars, points, quantiles),
                                     names=['par', 'point', 'quantile'])
out = pd.DataFrame(index=gi_table.index, columns=columns, dtype=np.float)

traces = jl.load('ramp_fits/traces/NEEM.gz').sel(param=pars)
start_tr = traces.sel(model='t0')
len_tr = traces.sel(model='dt')
end_tr = start_tr + len_tr
mid_tr = start_tr + 0.5 * len_tr

for tr, point in zip((start_tr, mid_tr, end_tr, len_tr),
                     ('start', 'mid', 'end', 'length')):
    for i in range(len(pars)):
        perc = np.percentile(tr[:, i, :], quantiles, axis=0)
        out.loc[:, (pars[i], point)] = perc.T

pd.concat((ages, out), axis=1).to_csv('results/NEEM_timing.csv',
                                      float_format='%.1f', mode='a')


# NGRIP lags
ref_par = 'Na'
pars = ['Ca', 'lt', 'd18O']
points = ['start', 'mid', 'end']
quantiles = np.array([50, 5, 95])
columns = pd.MultiIndex.from_product((pars, points, quantiles),
                                     names=['par', 'point', 'quantile'])
out = pd.DataFrame(index=gi_table.index, columns=columns, dtype=np.float)

traces = jl.load('ramp_fits/traces/NGRIP.gz').sel(param=[ref_par, ] + pars)

ref_start_tr = traces.sel(param=ref_par, model='t0').squeeze()
ref_len_tr = traces.sel(param=ref_par, model='t0').squeeze()
ref_end_tr = ref_start_tr + ref_len_tr
ref_mid_tr = ref_start_tr + 0.5 * ref_len_tr

start_tr = traces.sel(param=pars, model='t0')
len_tr = traces.sel(param=pars, model='dt')
end_tr = start_tr + len_tr
mid_tr = start_tr + 0.5 * len_tr

start_lag = start_tr - ref_start_tr
end_lag = end_tr - ref_end_tr
mid_lag = mid_tr - ref_mid_tr
for tr, l in zip((start_lag, mid_lag, end_lag), ('start', 'mid', 'end')):
    for i, p in enumerate(pars):
        perc = np.percentile(tr[:, i, :], quantiles, axis=0)
        out.loc[:, (p, l)] = perc.T

out.to_csv('results/NGRIP_lags.csv', float_format='%.1f', mode='a')

# NEEM lags
ref_par = 'Na'
pars = ['Ca', ]
points = ['start', 'mid', 'end']
quantiles = np.array([50, 5, 95])
columns = pd.MultiIndex.from_product((pars, points, quantiles),
                                     names=['par', 'point', 'quantile'])
out = pd.DataFrame(index=gi_table.index, columns=columns, dtype=np.float)

traces = jl.load('ramp_fits/traces/NEEM.gz').sel(param=[ref_par, ] + pars)

ref_start_tr = traces.sel(param=ref_par, model='t0').squeeze()
ref_len_tr = traces.sel(param=ref_par, model='t0').squeeze()
ref_end_tr = ref_start_tr + ref_len_tr
ref_mid_tr = ref_start_tr + 0.5 * ref_len_tr

start_tr = traces.sel(param=pars, model='t0')
len_tr = traces.sel(param=pars, model='dt')
end_tr = start_tr + len_tr
mid_tr = start_tr + 0.5 * len_tr

start_lag = start_tr - ref_start_tr
end_lag = end_tr - ref_end_tr
mid_lag = mid_tr - ref_mid_tr
for tr, l in zip((start_lag, mid_lag, end_lag), ('start', 'mid', 'end')):
    for i, p in enumerate(pars):
        perc = np.percentile(tr[:, i, :], quantiles, axis=0)
        out.loc[:, (p, l)] = perc.T

out.to_csv('results/NEEM_lags.csv', float_format='%.1f', mode='a')
