#!/bin/bash -e

mkdir -p ../tmp_scores_shuffle_seed

seed=$1

cd ../smith_waterman_3di

python ../py/smith_waterman_3di.py \
	--input scop40.3di.fa \
	--db scop40.3di.shuffle.fa \
	--samples 5000 \
	--seed $seed \
	--scores ../tmp_scores_shuffle_seed/scores_shuffle.seed$seed.txt
