# DO-progression

This repository contains all the data/code to reproduce the results for

*Erhardt, T., Capron, E., Rasmussen, S. O., Schüpbach, S., Bigler, M., Adolphi, F., and Fischer, H.: Decadal-scale progression of the onset of Dansgaard-Oeschger warming events, Clim. Past, 2019*

The easiest way to install all the requirements, is using `conda` and the provided `environment.yml` file that specifies the dependencies of the code.
To create a conda environment with the necessary packages run

    conda env create environment.yml

and to activate it
       
    source activate DO-progression

Running `make all` will than produce all the figures shown in the paper (in the folder 'figures/') as well as all supplementary files supplied with the paper (in the folder 'results/').

This will run the fitting, trace post processing and plotting scripts in that order.

**Warning**: Running the analysis can take a long time depending on your computer.
It will produce about 11 GB of intermediate results in the 'ramp_fits/samplers' and 'ramp_fits/traces' folders.
Restarting the analysis script will skip fits that where already run.

All sub directories contain their own respective `README.md` files:

- [code/README.md](code/README.md)
- [data/README.md](data/README.md)
- [ramp_fits/README.md](ramp_fits/README.md)
- [figures/README.md](figures/README.md)
- [results/README.md](results/README.md)

## Attribution
This code is associated and written for above mentioned paper.
If you make use of it, please cite the accompanying paper.

## License

Copyright 2019 Tobias Erhardt

The code in this repository is made available under the terms of the MIT License. 
For details, see LICENSE file.
