#!/bin/bash -e

cd ../plot_specs

python ../py/plot_dists_specs.py \
	../plots/C_F_score_selected_linscale.svg \
	C_F_score.reseekts \
	C_F_score.foldseekb \
	C_F_score.dali \
	C_F_score.tm
