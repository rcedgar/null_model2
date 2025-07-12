#!/bin/bash -e

cd ../plot_specs

python ../py/plot_dists_specs.py \
	../plots/C_score_F_selected_linscale.svg \
	C_score_F.reseekts \
	C_score_F.foldseekb \
	C_score_F.dali \
	C_score_F.tm
