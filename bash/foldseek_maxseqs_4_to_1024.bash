#!/bin/bash -e

qname=scop40
dbname=scop40

mkdir -p ../big_hits
mkdir -p ../P_prefilter
mkdir -p ../edf

q=../big_dbs/foldseek/$qname/$qname
db=../big_dbs/foldseek/$dbname/$dbname

for n in 4 8 16 32 64 128 512
do
	tmpdir=/tmp/foldseek_tmp
	rm -rf $tmpdir

	../bin/foldseek-v10 \
		easy-search \
		$q \
		$db \
		$hits \
		$tmpdir \
		--max-seqs $n \
		-e 10 \
		--format-output query,target,evalue,bits,prob

	rm -rf $tmpdir

	python ../py/empdist.py \
		--hits $hits \
		--lookup ../data/scop40.lookup \
		--fields 1,2,3 \
		--minevalue 1e-20 \
		--maxevalue 10 \
		--evalues \
		--output ../edf/foldseek_maxseqs$n.scop40.scop40.scop40
done

python ../py/plot_dists_specs.py \
	--spec ../plot_specs/P_F_score.foldseek_maxseqs \
	--plot ../P_prefilter/P_F_score.foldseek_maxseqs.svg
