#!/bin/bash -e

mkdir -p ../truth_standard_figures
cd ../truth_standard_figures

python ../py/truth_standard_figure.py \
	--hits ../big_hits/dali.scop40 \
	--minscore 6 \
	--delta 1 \
	--bins 12  \
	--xlabel "Z score" \
	--title "DALI SCOP40" \
	--plot dali.svg

python ../py/truth_standard_figure.py \
	--hits ../big_hits/tm.scop40 \
	--minscore 0.55 \
	--delta 0.01 \
	--bins 12  \
	--xlabel "TM score" \
	--title "TM-align SCOP40" \
	--plot tm.svg
