#!/bin/bash -e

lookup=../data/scop40.lookup
hits=../big_hits/blastp.scop40

mkdir -p ../edf

python ../py/empdist.py \
	--hits $hits \
	--lookup ../data/scop40.lookup \
	--fields 1,2,4 \
	--minscore 0 \
	--maxscore 250 \
	--output ../edf/blastp.scop40.scop40.scop40

python ../py/empdist.py \
	--hits $hits \
	--lookup ../data/scop40c.lookup \
	--fields 1,2,4 \
	--minscore 0 \
	--maxscore 250 \
	--output ../edf/blastp.scop40.scop40.scop40c

