#!/bin/bash -e

mkdir -p ../smith_waterman_3di_find_high_score_masked
cd ../smith_waterman_3di_find_high_score_masked

python ../py/smith_waterman_3di_find_high_score_masked.py \
	--seed $1 \
	--input ../smith_waterman_3di/scop40.3di.segmask.fa \
	--output high_score_masked_seed$1.txt
