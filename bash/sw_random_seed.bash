#!/bin/bash -e

mkdir -p ../tmp_scores_random_seed

seed=$1

cd ../smith_waterman_3di

python ../py/smith_waterman_3di_random.py \
	--samples 5000 \
	--seed $seed \
	--scores ../tmp_scores_random_seed/scores_random.seed$seed.txt
