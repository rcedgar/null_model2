#!/bin/bash -e

lookup=../data/scop40.lookup
hits=../big_hits/blastp.scop40

mkdir -p ../edf

python ../py/empdist.py \
	--hits $hits \
	--lookup ../data/scop40.lookup \
	--fields 1,2,3 \
	--evalues \
	--minevalue 1e-40 \
	--maxevalue 10 \
	--output ../edf/blastpe.scop40
