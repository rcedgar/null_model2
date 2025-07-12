#!/bin/bash -e

mkdir -p ../foldseek_evalue_test
cd ../foldseek_evalue_test

## grep "^d1h1oa2.*AF-A0A6N9R5S2-F1-model_v4" foldseek_exhaustive_scop40_vs_afdb.tsv \
## 	| tee afdb.txt
## d1h1oa2/a.3.1.4 AF-A0A6N9R5S2-F1-model_v4       8.044E-05       222     1.000

for v in 8 9 10
do
	rm -rf ../foldseek_tmp
	mkdir -p ../foldseek_tmp

	foldseek-v$v \
		easy-search \
		d1h1oa2.pdb \
		AF-A0A6N9R5S2-F1-model_v4.pdb \
		v$v.tsv \
		/tmp \
		-e 10 \
		--format-output query,target,evalue \
		> stdout.v$v \
		2> stderr.v$v

	foldseek-v$v \
		easy-search \
		AF-A0A6N9R5S2-F1-model_v4.pdb \
		d1h1oa2.pdb \
		vrev$v.tsv \
		/tmp \
		-e 10 \
		--format-output query,target,evalue \
		> stdout.vrev$v \
		2> stderr.vrev$v

	foldseek-v$v \
		easy-search \
		d1h1oa2.pdb \
		AF-A0A6N9R5S2-F1-model_v4.pdb \
		x$v.tsv \
		/tmp \
		-e 10 \
		--exhaustive-search 1 \
		--format-output query,target,evalue \
		> stdout.x$v \
		2> stderr.x$v

	foldseek-v$v \
		easy-search \
		AF-A0A6N9R5S2-F1-model_v4.pdb \
		d1h1oa2.pdb \
		xrev$v.tsv \
		/tmp \
		-e 10 \
		--exhaustive-search 1 \
		--format-output query,target,evalue \
		> stdout.xrev$v \
		2> stderr.xrev$v

	rm -rf ../foldseek_tmp
done

grep . *.tsv
