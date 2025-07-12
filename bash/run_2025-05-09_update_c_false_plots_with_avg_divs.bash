#!/bin/bash -e

# c5d913f + 1

name=2025-05-09_update_c_false_plots_with_avg_divs
rundir=../runs/$name
mkdir -p $rundir

rm -rf ../edfs
rm -rf ../plots

./edfs.bash
./edf_avgs.bash
./c_false_plots.bash

date \
	> $rundir/date.txt

git log \
	| head \
	> $rundir/git_log.txt

cp -vr ../plots $rundir
cp -vr ../edf $rundir

./sync_to_s3.bash
