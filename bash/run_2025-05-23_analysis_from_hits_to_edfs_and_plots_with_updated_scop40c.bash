#!/bin/bash -e

# 28a47cb + 1

if [ "$CONDA_DEFAULT_ENV" != null_model ] ; then
	echo Must conda activate null_model
	exit 1
fi

name=2025-05-23_analysis_from_hits_to_edfs_and_plots_with_updated_scop40c
rundir=../runs/$name

rm -rf $rundir
mkdir -p $rundir

date > $rundir/date.txt

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
./top_fps_scop40c.bash

python ../py/plot_cves_scop40_algos.py scop40
python ../py/plot_cves_scop40_algos.py scop40c

git log \
	| head -n 20 \
	> $rundir/git_log.txt

cp -vr ../plots $rundir
cp -vr ../edf $rundir
cp -vr ../fit_gumbel $rundir
cp -vr ../fit_loglin $rundir
cp -vr ../cves $rundir

date >> $rundir/date.txt

# ./sync_to_s3.bash
