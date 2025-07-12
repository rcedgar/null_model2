#!/bin/bash -e

cd ../big_hits

for hits in \
	reseek_verysensitive.scop40
do
	python ../py/scop40c_subset_hits.py $hits \
		> ${hits}c
done

ls -ltrh
