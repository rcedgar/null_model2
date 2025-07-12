#!/bin/bash -e

mkdir -p ../edf

lookup=../data/scop40.lookup
hits=../big_data/hits/foldseek_dpscore.scop40.scop40

python ../py/empdist.py \
	--hits $hits \
	--lookup $lookup \
	--fields 1,2,3 \
	--minscore 0 \
	--maxscore 300 \
	--output ../edf/foldseek_dpscore.scop40.scop40.scop40

ls -lh ../edf/foldseek_dpscore.scop40.scop40.scop40

exit 1 ####################################################

python ../py/empdist.py \
	--hits $hits \
	--lookup $lookup \
	--fields 1,2,4 \
	--minscore -100 \
	--maxscore 200 \
	--output ../edf/foldseek_diffscore.scop40.scop40.scop40

ls -lh ../edf/foldseek_diffscore.scop40.scop40.scop40
