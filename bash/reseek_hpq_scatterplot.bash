#!/bin/bash -e

mkdir -p ../tmp

echo ../edf/reseek.cath40 > ../tmp/edfs.tmp
echo ../edf/reseek.scop40 >> ../tmp/edfs.tmp
echo ../edf/reseek.scop40.n2 >> ../tmp/edfs.tmp
echo ../edf/reseek.scop40.n4 >> ../tmp/edfs.tmp
echo ../edf/reseek.scop40x4 >> ../tmp/edfs.tmp
echo ../edf/reseek.scop40x8 >> ../tmp/edfs.tmp
echo ../edf/reseek_fast.scop40_afdb50 >> ../tmp/edfs.tmp
echo ../edf/reseek_fast.scop40_bfvd >> ../tmp/edfs.tmp
echo ../edf/reseek_fast.scop40_pdb >> ../tmp/edfs.tmp

echo ".CATH40" > ../tmp/labels.tmp
echo ".SCOP40" >> ../tmp/labels.tmp
echo "./2" >> ../tmp/labels.tmp
echo "./4" >> ../tmp/labels.tmp
echo ".X4" >> ../tmp/labels.tmp
echo ".X8" >> ../tmp/labels.tmp
echo ".AFDB50" >> ../tmp/labels.tmp
echo ".BFVD" >> ../tmp/labels.tmp
echo ".PDB" >> ../tmp/labels.tmp

mkdir -p ../hpq_scatterplot
cd ../hpq_scatterplot

python ../py/hpq_scatterplot.py  \
	--plot reseek_hpq_scatter.svg \
	--title Reseek \
	--prefilter_size 1500 \
	--yrange 5:2000 \
	--edfs `cat ../tmp/edfs.tmp` \
	--labels `cat ../tmp/labels.tmp` \
	--output reseek.tsv
