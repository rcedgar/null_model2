#!/bin/bash -e

cd ../big_hits

for hits in \
	dali.scop40 \
	foldseek.scop40 \
	reseek.scop40 \
	tm.scop40
do
	python ../py/scop40c_subset_hits.py $hits \
		> ${hits}c
done

ls -ltrh
