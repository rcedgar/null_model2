#!/bin/bash -e

q=scop40
db=scop40

mkdir -p ../big_hits
mkdir -p ../log
mkdir -p ../P_prefilter
mkdir -p ../edf

for size in 4 8 16 32 64 128 256 512 1024
do
	name=rsbsize$size
	hits=../big_hits/reseek_rsbsize$size.scop40.scop40 \

	reseek \
		-search ../big_dbs/reseek/$q.bca \
		-db ../big_dbs/reseek/${db}.bca \
		-output $hits \
		-fast \
		-mints 0.05 \
		-rsb_size $size \
		-columns query+target+evalue+dpscore+newts \
		-log ../log/$name

	ls -lh $hits

	python ../py/empdist.py \
		--hits $hits \
		--lookup ../data/scop40.lookup \
		--fields 1,2,5 \
		--minscore 0.05 \
		--maxscore 1.05 \
		--output ../edf/reseek_${name}_ts.scop40.scop40.scop40

	python ../py/reseek_P_pass_prefilter_edfs.py \
		scop40 scop40 $name \
		> ../P_prefilter/$name.tsv

	ls -lh ../P_prefilter/$name.tsv
done

python ../py/plot_prefilter_rsbsizes_and_afdb.py

python ../py/plot_dists_specs.py \
	--spec ../plot_specs/P_F_score.reseek_rsbsizes \
	--plot ../P_prefilter/P_F_score.reseek_rsbsizes.svg
