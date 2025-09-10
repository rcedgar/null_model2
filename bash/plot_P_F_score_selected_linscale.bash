#!/bin/bash -e

cd ../plot_specs

python ../py/plot_dists_specs.py \
	--plot ../plots/P_F_score_selected_linscale.svg \
	--specs \
		../plot_specs/P_F_score.foldseek_default \
		../plot_specs/P_F_score.reseek_sensitive \
		../plot_specs/P_F_score.dali \
		../plot_specs/P_F_score.tm
