#!/bin/bash -e

pre=../big_data/hits/foldseek_default.scop40.afdb50
all=../big_data/hits/foldseek_exhaustive_scop40_vs_afdb.tsv

if [ ! -s $pre ] ; then
	echo Not found pre=$pre
	exit 1
fi

if [ ! -s $all ] ; then
	echo Not found all=$all
	exit 1
fi

mkdir -p ../tmp
mkdir -p ../P_prefilter
cd ../P_prefilter

python ../py/subsample_all_pre_hits.py \
	--hits_all $all \
	--hits_pre $pre \
	--out_all ../tmp/foldseek_out_all.tsv \
	--out_pre ../tmp/foldseek_out_pre.tsv

python ../py/scores_hist.py \
	--scores ../tmp/foldseek_out_pre.tsv \
	--field 4 \
	--evalues \
	--minscore -1 \
	--binwidth 0.2 \
	--bins 100 \
	--output foldseek_hist_pre.tsv

python ../py/scores_hist.py \
	--scores ../tmp/foldseek_out_all.tsv \
	--field 3 \
	--evalues \
	--minscore -1 \
	--binwidth 0.2 \
	--bins 100 \
	--output foldseek_hist_all.tsv

python ../py/P_prefilter.py \
	--edf ../edf/foldseek_default.scop40.scop40.scop40 \
	--hist_all foldseek_hist_all.tsv \
	--hist_pre foldseek_hist_pre.tsv  \
	> foldseek_P_prefilter.tsv
