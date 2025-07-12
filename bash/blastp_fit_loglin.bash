#!/bin/bash -e

mkdir -p ../fit_loglin
cd ../fit_loglin

python ../py/loglin_fit_c_score_f.py \
	--edf ../edf/blastp.scop40.scop40.scop40 \
	--output blastp.scop40.tsv \
	--plot blastp.scop40.svg,blastp.scop40.png \
	--title "BLASTP SCOP40" \
	--xlabel "Raw score" \
	--fitlo 55 \
	--fithi 80 \
	--xrange 30:100

python ../py/loglin_fit_c_score_f.py \
	--edf ../edf/blastp.scop40.scop40.scop40c \
	--output blastp.scop40c.tsv \
	--plot blastp.scop40c.svg,blastp.scop40c.png \
	--title "BLASTP SCOP40c" \
	--xlabel "Raw score" \
	--fitlo 55 \
	--fithi 80 \
	--xrange 30:100
