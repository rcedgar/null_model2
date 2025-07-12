#!/bin/bash -e

mkdir -p ../tmp

echo ../edf/foldseek.cath40 > ../tmp/edfs.tmp
echo ../edf/foldseek.scop40 >> ../tmp/edfs.tmp
echo ../edf/foldseek.scop40.n2 >> ../tmp/edfs.tmp
echo ../edf/foldseek.scop40.n4 >> ../tmp/edfs.tmp
echo ../edf/foldseek.scop40x4 >> ../tmp/edfs.tmp
echo ../edf/foldseek.scop40x8 >> ../tmp/edfs.tmp
echo ../edf/foldseek.scop40_afdb50 >> ../tmp/edfs.tmp
echo ../edf/foldseek.scop40_bfvd >> ../tmp/edfs.tmp
echo ../edf/foldseek.scop40_pdb >> ../tmp/edfs.tmp

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
	--plot foldseek_hpq_scatter.svg \
	--title Foldseek \
	--yrange 50:1500 \
	--prefilter_size 1000 \
	--edfs `cat ../tmp/edfs.tmp` \
	--labels `cat ../tmp/labels.tmp` \
	--output foldseek.tsv
