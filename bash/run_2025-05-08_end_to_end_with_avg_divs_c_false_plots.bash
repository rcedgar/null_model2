#!/bin/bash -e

# c5d913f + 1

name=2025-05-08_end_to_end_with_avg_divs_c_false_plots
rundir=../runs/$name

######################################################
rm -rf ../big_*
######################################################


rm -rf $rundir
mkdir -p $rundir

rm -rf ../edfs
rm -rf ../plots
mkdir -p ../log
mkdir -p ../tmp

./download_dali_and_tm_hits.bash

./setup_cath40.bash
./setup_scop40.bash
./setup_scop95.bash
./setup_scop40x8.bash

./reseek_search.bash cath40
./reseek_search.bash scop40
./reseek_search.bash scop95
./reseek_search_x8.bash

./foldseek_search.bash cath40
./foldseek_search.bash scop40
./foldseek_search.bash scop95
./foldseek_search_scop40x8.bash

./edfs.bash
./edf_avgs.bash
./c_false_plots.bash

date \
	> $rundir/date.txt

git log \
	| head -n 20 \
	> $rundir/git_log.txt

cp -vr ../plots $rundir
cp -vr ../edf $rundir

# ./sync_to_s3.bash
