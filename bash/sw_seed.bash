#!/bin/bash -e

mkdir -p ../tmp_scores_seed
mkdir -p ../tmp_scores_segmask_deleted_seed
mkdir -p ../tmp_scores_shuffle_seed

seed=$1

cd ../smith_waterman_3di

python ../py/smith_waterman_3di.py \
	--input scop40.3di.fa \
	--db scop40.3di.reverse.fa \
	--samples 5000 \
	--seed $seed \
	--scores ../tmp_scores_seed/scores.seed$seed.txt

python ../py/smith_waterman_3di.py \
	--input scop40.3di.segmask_deleted.fa \
	--db scop40.3di.reverse.segmask_deleted.fa \
	--samples 5000 \
	--seed $seed \
	--scores ../tmp_scores_segmask_deletd_seed/scores_segmask_deleted.seed$seed.txt

python ../py/smith_waterman_3di.py \
	--input scop40.3di.fa \
	--db scop40.3di.shuffle.fa \
	--samples 5000 \
	--seed $seed \
	--scores ../tmp_scores_shuffle_seed/scores_shuffle.seed$seed.txt
