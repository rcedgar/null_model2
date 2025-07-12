#!/bin/bash -e

cd ../smith_waterman_3di

python ../py/scores_hist.py \
	--scores scores.txt \
	--minscore 0 \
	--binwidth 20 \
	--bins 100 \
	--output scores_hist.tsv

python ../py/scores_hist.py \
	--scores scores_segmask_deleted.txt \
	--minscore 0 \
	--binwidth 20 \
	--bins 100 \
	--output scores_segmask_deleted_hist.tsv

python ../py/gumbel_fit_histogram_with_residuals.py \
	--hist scores_hist.tsv \
	--plot \
		gumbel_fit_not_masked.svg \
		gumbel_fit_not_masked.png \
	--barwlin 16 \
	--barwlog 16 \
	--xrange_lin 0:1200 \
	--xrange_log 0:1200 \
	--yrange_lin 1:150000 \
	--yrange_log 1:5e5 \
	--plot_w 7 \
	--plot_h 2 \
	--nofilename

python ../py/gumbel_fit_histogram_with_residuals.py \
	--hist scores_segmask_deleted_hist.tsv \
	--plot \
		gumbel_fit_segmasked.svg \
		gumbel_fit_segmasked.png \
	--barwlin 16 \
	--barwlog 16 \
	--xrange_lin 0:1200 \
	--xrange_log 0:1200 \
	--yrange_lin 1:200000 \
	--yrange_log 1:1e6 \
	--plot_w 7 \
	--plot_h 2 \
	--nofilename
