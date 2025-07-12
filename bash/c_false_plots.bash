#!/bin/bash -e

mkdir -p ../plots

for algo in reseek reseekts foldseek foldseekb dali tm
do
	for plot in C_score_F C_F_score
	do
		./plot_spec.bash $plot.$algo
	done
done
