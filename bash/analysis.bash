#!/bin/bash -e

# blastp align and analyze
./run_blastp.bash

# Emprical distributions
./edfs.bash
./edf_blastp.bash
./plot_hitrates.bash
./C_score_F.bash
./P_T_score.bash
./truth_figures.bash

# Fit EVD
./smith_waterman_3di_fit_gumbel.bash
./reseekdp_fit_gumbel.bash
./foldseekdp_fit_gumbel.bash
./fit_gumbels_summary_png.bash

# Fit log-linear
./fit_loglins.bash
./make_fitted_params.bash

# Pre-filter empirical results
./make_reseek_afdb100k_subset.bash
./prefilter_sizes_report.bash
./prefilter_top_hits.bash
./reseek_P_pass_prefilter.bash

# E-values vs. measured FPEPQ
./evalue_vs_epq.bash

# CVE plots
./cves.bash

# Validate
./predict_FPEPQs.bash

# Extrapolate to PDB and AFDB
./foldseek_rescale_evalue.bash
./bayes_evalue_table.bash

./reseek_calibrate.bash
