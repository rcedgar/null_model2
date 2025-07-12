#!/bin/bash -e

# 46ff0eb + 1

source activate base
conda activate pymoo

name=2025-05-19_analysis_from_hits_to_edfs_and_plots_with_scop40c
rundir=../runs/$name

rm -rf $rundir
mkdir -p $rundir

rm -rf ../edfs
rm -rf ../plots
mkdir -p ../log
mkdir -p ../tmp

./edfs.bash
./edf_avgs.bash
./c_false_plots.bash
./fit_gumbels.bash
./fit_loglins.bash
./fit_gumbels_scop40c.bash
./fit_loglins_scop40c.bash
./top_fps.bash

date \
	> $rundir/date.txt

git log \
	| head -n 20 \
	> $rundir/git_log.txt

cp -vr ../plots $rundir
cp -vr ../edf $rundir
cp -vr ../fit_gumbel $rundir
cp -vr ../fit_loglin $rundir

# ./sync_to_s3.bash
