#!/bin/bash -e

cd ../plot_specs

python ../py/plot_dists_specs.py \
	../plots/P_T_score_selected_linscale.svg \
	P_T_score.reseekts \
	P_T_score.foldseekb \
	P_T_score.dali \
	P_T_score.tm
