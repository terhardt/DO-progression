"""Inference script

The script reads in the data file(s) passed in as command line arguments
and runs the MCMC fitting routine on each data series of the file in parallel.

The emcee.EnsembleSampler objects are than dumped in on compressed file to disk
for later processing

skips input files where the resulting sampler file already exists

Usage:
    python run_inference.py ramp_fits/data/*.csv
"""
import sys
from os.path import splitext, basename, exists
import pandas as pd
import joblib as jl
from code.model import fit_mcmc


def process_input_file(data_file):
    sampler_name = splitext(basename(data_file))[0]
    sampler_file = 'ramp_fits/sampler/{:s}.gz'.format(sampler_name)
    t, y = pd.read_csv(data_file, header=None).values.T
    sampler = fit_mcmc(t, y, nsample=60000)
    jl.dump((sampler_name, sampler), sampler_file, compress=4)
    return sampler_file


def filter_file_list(data_files):
    new_list = []
    for data_file in data_files:
        sampler_name = splitext(basename(data_file))[0]
        sampler_file = 'ramp_fits/sampler/{:s}.gz'.format(sampler_name)
        if exists(sampler_file):
            print('Skipping %s' % data_file)
        else:
            new_list.append(data_file)
    return new_list


if __name__ == "__main__":
    if len(sys.argv) == 1:
        from glob import glob
        data_files = glob('data/ramp_data/*.csv')
    else:
        data_files = sys.argv[1:]

    data_files = filter_file_list(data_files)
    print('Number of data files: %g' % len(data_files))

    with jl.Parallel(n_jobs=4, verbose=20) as par:
        par(jl.delayed(process_input_file)(data_file)
            for data_file in data_files)
