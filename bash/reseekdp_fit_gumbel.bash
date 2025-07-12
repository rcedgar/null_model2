#!/usr/bin/bash -e

mkdir -p ../fit_gumbel
cd ../fit_gumbel

# sensitive does not fit Gumbel well, included for the record
# verysensitive is needed to avoid biased low-scoring filter
for mode in sensitive verysensitive
do
	hits=../big_hits/reseek_$mode.scop40.scop40

	python ../py/score_F_hist.py \
		--hits $hits \
		--minscore 5 \
		--maxscore 200 \
		--fields 1,2,4 \
		--bins 100 \
		--output reseekdp_$mode.hist

	python ../py/gumbel_fit_histogram_with_residuals.py \
		--hist reseekdp_$mode.hist \
		--output reseekdp_$mode.tsv \
		--plot \
			reseekdp_$mode.svg \
			reseekdp_$mode.png \
		--nofilename \
		--title "Reseek SCOP40" \
		--xlabel "S-W score" \
		--minscore 5 \
		--maxscore 100 \
		--xrange_lin 5:50 \
		--xrange_log 5:100 \
		--yrange_log 100:1e7 \
		--barwlin 1.5 \
		--barwlog 1.2
done
