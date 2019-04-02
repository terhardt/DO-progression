import numpy as np
import joblib as jl
import xarray as xr
import pandas as pd
import sys
from os.path import exists
from itertools import product


def get_traces(sampler, nthin):
    """Extract traces from emcee.EnsebleSampler and apply
    invers transformation of parameters
    """
    # load every nthin'th sample from the walkers and reshape to
    # final dimensions
    traces = sampler.chain[:, ::nthin, :].reshape(-1, sampler.dim).copy()
    # convert from sample space to meaningfull space
    traces[:, [1, 4, 5]] = np.exp(traces[:, [1, 4, 5]])
    return traces


if __name__ == '__main__':
    try:
        CORE = sys.argv[1]
    except IndexError:
        print('Please give core name as argument')
        sys.exit(1)

    # Load event table
    events = pd.read_table('data/GIS_table.txt', usecols=(0, ),
                           squeeze=True, comment='#').values
    # initiate the output data array
    events = np.array(events)
    params = np.array(('Ca', 'Na', 'lt', 'd18O'))
    model  = np.array(('t0', 'dt', 'y0', 'dy', 'tau', 'sigma'))
    output_shape = (6000, len(model), len(params), len(events))
    da = xr.DataArray(np.full(output_shape, np.nan),
                      dims=('sample', 'model', 'param', 'event'),
                      coords={'model': model,
                              'param': params,
                              'event': events})

    sf_str = 'ramp_fits/sampler/{:s}_{:s}_{:s}.gz'
    # Load all samplers, extract traces and put into the DataArray
    for p, e in product(params, events):
        f = sf_str.format(CORE, e, p)
        if not exists(f):
            continue
        print('loading %s' % f)
        _, sampler = jl.load(f)
        if sampler.acceptance_fraction.mean() <= 0.3:
            print('\t skipping %s' % f)
            print('\t Acceptance fraction: %f' % (
                  sampler.acceptance_fraction.mean()))
            continue
        else:
            traces = get_traces(sampler, nthin=600)
            da.sel(param=p, event=e)[:, :] = traces
    # Save data array to disk for later use
    trace_file = 'ramp_fits/traces/{:s}.gz'.format(CORE)
    print('saving traces to %s' % trace_file)
    jl.dump(da, trace_file, compress=3)
