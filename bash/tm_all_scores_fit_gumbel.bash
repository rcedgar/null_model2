#!/bin/bash -e

mkdir -p ../tm_all_scores_fit_gumbel
cd ../tm_all_scores_fit_gumbel

if [ ! -s scores_hist.tsv ] ; then
	python ../py/scores_hist.py \
		--scores $src/null_model/big_hits/tm.scop40 \
		--field 3 \
		--minscore 0 \
		--binwidth 0.01 \
		--bins 100 \
		--output scores_hist.tsv
fi

# How significant is a protein structure similarity with TM-score = 0.5?
# doi:10.1093/bioinformatics/btq066
#   0.0242  location (mu)
#   0.0152  scale (beta)

# Results from fitting below to SCOP40 all-vs-all:
#   0.02602  mu
#   0.03723  beta
# 1.226e+06  norm
#    0.2283  center

python ../py/gumbel_fit_histogram_with_residuals.py \
	--hist scores_hist.tsv \
	--plot \
		gumbel_fit.svg \
		gumbel_fit.png \
	--xrange_lin 0.1:0.5 \
	--xrange_log 0:0.9 \
	--yrange_log 0:1e8 \
	--barwlin 0.005 \
	--barwlog 0.005 \
	--plot_w 7 \
	--plot_h 2 \
	--nofilename
