.PHONY: clean

all: sampler traces figures results

clean_traces:
	rm -f ramp_fits/traces/*.gz
	rm -f ramp_fits/sampler/*.gz

sampler: data/ramp_data
	python run_inference.py

traces: ramp_fits/traces/NEEM.gz ramp_fits/traces/NGRIP.gz

ramp_fits/traces/NEEM.gz: ramp_fits/sampler
	python process_ramp_samplers.py NEEM

ramp_fits/traces/NGRIP.gz: ramp_fits/sampler
	python process_ramp_samplers.py NGRIP


figures : figures/fig_01_overview.pdf figures/fig_02_example_fit.pdf figures/fig_03_timing_diffs.pdf figures/fig_04_combined_evidence.pdf figures/fig_05_order.pdf figures/fig_S01_SNR_uncert_NGRIP.pdf figures/fig_S02_SNR_lag_NGRIP.pdf

figures/fig_01_overview.pdf: fig_01_overview.py data/NGRIP_10yr.csv data/NEEM_10yr.csv
	python fig_01_overview.py

figures/fig_03_timing_diffs.pdf: fig_03_timing_diffs.py ramp_fits/traces/NGRIP.gz ramp_fits/traces/NEEM.gz
	python fig_03_timing_diffs.py

figures/fig_02_example_fit.pdf: fig_02_example_fit.py ramp_fits/traces/NGRIP.gz ramp_fits/traces/NEEM.gz
	python fig_02_example_fit.py

figures/fig_04_combined_evidence.pdf: fig_04_combined_evidence.py ramp_fits/traces/NGRIP.gz ramp_fits/traces/NEEM.gz
	python fig_04_combined_evidence.py

figures/fig_05_order.pdf: fig_05_order.py ramp_fits/traces/NGRIP.gz ramp_fits/traces/NEEM.gz
	python fig_05_order.py

figures/fig_S01_SNR_uncert_NGRIP.pdf: fig_S01_SNR_uncert_NGRIP.py ramp_fits/traces/NGRIP.gz ramp_fits/traces/NEEM.gz
	python fig_S01_SNR_uncert_NGRIP.py

figures/fig_S02_SNR_lag_NGRIP.pdf: fig_S02_SNR_lag_NGRIP.py ramp_fits/traces/NGRIP.gz ramp_fits/traces/NEEM.gz
	python fig_S02_SNR_lag_NGRIP.py

results: ramp_fits/traces/NEEM.gz ramp_fits/traces/NGRIP.gz
	python suppl_tables.py

clean: 
	rm -f figures/*.pdf
	rm -f results/*.csv
