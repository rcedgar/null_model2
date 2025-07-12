#!/bin/bash -e

mkdir -p ../P_T_score
mkdir -p ../summary_pngs

python ../py/plot_dists_specs.py \
	--plot ../P_T_score/P_T_score.svg,../summary_pngs/P_T_score.png \
	--cols 2 \
	--specs \
		../plot_specs/P_T_score.dali \
		../plot_specs/P_T_score.tm \
		../plot_specs/P_T_score.foldseek_exhaustive \
		../plot_specs/P_T_score.reseek_sensitive
