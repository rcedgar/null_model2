#!/bin/bash -e

name=run_2025-06-01_alignments
rundir=../runs/$name

rm -rf $rundir
mkdir -p $rundir

date > $rundir/date_started.txt

#######################################
# TODO
# ./download_dali_and_tm_hits.bash
# ./download_afdb_hits.bash
#######################################

./foldseek_and_reseek_searches.bash

git log \
	| head -n 20 \
	> $rundir/git_log.txt

ls -lh ../big_hits \
	> $rundir/big_hits.ls

cp -vr ../bash/ $rundir

date > $rundir/date_finished.txt
