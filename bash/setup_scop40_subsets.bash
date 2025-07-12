#!/bin/bash -e

mkdir -p ../scop40_subsets
cd ../scop40_subsets

for k in 2 4
do
	n=$((11211/$k))
	echo "__________________________"
	echo k=$k n=$n
	echo "--------------------------"
	python ../py/cal_subsample.py \
		../big_data/scop40.fs.cal \
		$n \
		> scop40_div$k.cal
	
	grep "^>" scop40_div$k.cal \
		| tr -d '>' \
		| sort \
		> scop40_div$k.doms
	
	fgrep -Ff scop40_div$k.doms ../data/scop40.lookup \
		> ../data/scop40_div$k.lookup

	reseek \
		-convert scop40_div$k.cal \
		-bca ../big_dbs/reseek/scop40_div$k.bca

	mkdir -p ../big_dbs/foldseek/scop40_div$k
	reseek \
		-create_foldseekdb ../big_dbs/reseek/scop40_div$k.bca \
		-3di ../big_data/scop40.3di.fa \
		-output ../big_dbs/foldseek/scop40_div$k/scop40_div$k
done
