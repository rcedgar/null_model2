#!/usr/bin/bash -e

mkdir -p ../fit_gumbel
cd ../fit_gumbel

hits=../big_data/hits/foldseek_dpscore.scop40.scop40

if [ ! -s foldseek_dpscore.hist ] ; then
	python ../py/score_F_hist.py \
		--hits $hits \
		--minscore 0 \
		--maxscore 300 \
		--fields 1,2,3 \
		--bins 100 \
		--output foldseek_dpscore.hist
fi

python ../py/gumbel_fit_histogram_with_residuals.py \
	--hist foldseek_dpscore.hist \
	--output foldseek_dpscore.tsv \
	--plot \
		foldseek_dpscore.svg \
		foldseek_dpscore.png \
	--nofilename \
	--title "Foldseek SCOP40" \
	--xlabel "S-W score" \
	--minscore 0 \
	--maxscore 100 \
	--xrange_lin 1:200 \
	--xrange_log 1:200 \
	--yrange_log 1e4:1e7 \
	--barwlin 1.5 \
	--barwlog 1.2

if [ ! -s foldseek_diffscore.hist ] ; then
	python ../py/score_F_hist.py \
		--hits $hits \
		--minscore -100 \
		--maxscore 200 \
		--fields 1,2,4 \
		--bins 100 \
		--output foldseek_diffscore.hist
fi

python ../py/gumbel_fit_histogram_with_residuals.py \
	--hist foldseek_diffscore.hist \
	--output foldseek_diffscore.tsv \
	--plot \
		foldseek_diffscore_with_residuals.svg \
		foldseek_diffscore_with_residuals.png \
	--nofilename \
	--title "Foldseek SCOP40" \
	--xlabel "Diff score" \
	--minscore 0 \
	--maxscore 100 \
	--xrange_lin _100:100 \
	--xrange_log _100:100 \
	--yrange_log 1e4:1e7 \
	--barwlin 1.5 \
	--barwlog 1.2

python ../py/gumbel_fit_histogram.py \
	--hist foldseek_diffscore.hist \
	--output foldseek_diffscore.tsv \
	--plot \
		foldseek_diffscore.svg \
		foldseek_diffscore.png \
	--nofilename \
	--title "Foldseek SCOP40" \
	--xlabel "Diff score" \
	--minscore -100 \
	--maxscore 200 \
	--xrange_lin _30:80 \
	--xrange_log _100:200 \
	--yrange_log 1e2:1e8 \
	--barwlin 2.1 \
	--barwlog 1.2
