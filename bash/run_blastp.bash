#!/bin/bash -e

date > ../tmp/blastp.date

mkdir -p ../big_hits

rm -f ../big_hits/blastp*
rm -f ../edf/blastp*
rm -f ../fit_gumbel/blastp*
rm -f ../fit_loglin/blastp*

blastp \
	-query ../data/scop40.fa \
	-subject ../data/scop40.fa \
	-evalue 10 \
	-outfmt "6 qseqid sseqid evalue score" \
	> ../big_hits/blastp.scop40

./edf_blastp.bash
./edf_blastpe.bash
./blastp_fit_loglin.bash

python ../py/blastp_add_predicted_FPEPQ_to_hits.py \
	> ../big_hits/blastpx.scop40

./edf_blastpx.bash

date >> ../tmp/blastp.date
cat ../tmp/blastp.date
