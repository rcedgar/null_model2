#!/bin/bash -e

cd ../plot_specs

python ../py/plot_dists_specs.py \
	../plots/C_T_score_selected_linscale.svg \
	C_T_score.reseekts \
	C_T_score.foldseekb \
	C_T_score.dali \
	C_T_score.tm
