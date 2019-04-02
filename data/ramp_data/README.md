# Ramp Data

This folder contains the data for each of the parameters for the individual transitions.
These are used as input files for the `run_inference.py` script.

All files contain two columns.
The first column provides the time relative to the absolute age of the transition, the second column
contains the data that the ramp is fitted to.
In the case of Ca, Na and annual layer thickness, this data is the log of the respective data.

The files are named to reflect their content, e.g:

    NEEM_GI-1e_Ca.csv

contains the (log transformed) Ca record from NEEM for the transition into GI-1e.
