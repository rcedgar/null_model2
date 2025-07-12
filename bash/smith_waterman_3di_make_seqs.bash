#!/bin/bash -e

mkdir -p ../smith_waterman_3di
cd ../smith_waterman_3di

cp -v ../data/scop40.3di.fa .

python ../py/fasta2aafreqs.py scop40.3di.fa \
	| tee ../smith_waterman_3di/3di_freqs.txt

python ../py/smith_waterman_3di.py \
    --input scop40.3di.fa \
	--seed 1 \
    --shuffle scop40.3di.shuffle.fa

segmasker \
	-in scop40.3di.fa \
	-outfmt fasta \
	-out scop40.3di.segmask.fa

segmasker \
	-in scop40.3di.reverse.fa \
	-outfmt fasta \
	-out scop40.3di.reverse.segmask.fa

python ../py/smith_waterman_3di.py \
	--input scop40.3di.segmask.fa \
	--delete_segmask \
	--output scop40.3di.segmask_deleted.fa

python ../py/smith_waterman_3di.py \
	--input scop40.3di.segmask.fa \
	--delete_segmask \
	--output scop40.3di.segmask_deleted.fa

python ../py/smith_waterman_3di.py \
	--input scop40.3di.reverse.segmask.fa \
	--delete_segmask \
	--output scop40.3di.reverse.segmask_deleted.fa
