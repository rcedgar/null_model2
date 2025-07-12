#!/bin/bash -e

mkdir -p ../estimated_evalues
cd ../estimated_evalues

python ../py/estimated_evalues.py \
	--algo dali \
	--targets scop40 \
	--loscore 2 \
	--delta 2 \
	--nrscores 20 \
	--xrange 2:30 \
	--output dali.tsv \
	--plot dali.svg

python ../py/estimated_evalues.py \
	--algo tm \
	--targets scop40 \
	--loscore 0.2 \
	--delta 0.1 \
	--xrange 0.3:1.0 \
	--nrscores 8 \
	--output tm.tsv \
	--plot tm.svg

python ../py/estimated_evalues.py \
	--algo foldseek \
	--targets scop40,scop40_afdb50 \
	--evalues \
	--loscore -1 \
	--delta 1 \
	--nrscores 14 \
	--yrange 1e-3:1e3 \
	--output foldseek.tsv \
	--plot foldseek.svg

python ../py/estimated_evalues.py \
	--algo reseek_fast \
	--targets scop40,scop40_afdb50 \
	--evalues \
	--loscore -1 \
	--delta 1 \
	--nrscores 8 \
	--output reseek_fast.tsv \
	--plot reseek_fast.svg
