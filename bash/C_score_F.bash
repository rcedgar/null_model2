#!/bin/bash -e

mkdir -p ../C_score_F
mkdir -p ../summary_pngs

python ../py/plot_dists_specs.py \
	--plot ../C_score_F/C_score_F.svg,../summary_pngs/C_score_F.png \
	--specs \
		../plot_specs/C_score_F.dali \
		../plot_specs/C_score_F.tm \
		../plot_specs/C_score_F.foldseek_exhaustive \
		../plot_specs/C_score_F.reseek_sensitive \
		../plot_specs/C_score_F.foldseek_default \
		../plot_specs/C_score_F.reseek_fast
