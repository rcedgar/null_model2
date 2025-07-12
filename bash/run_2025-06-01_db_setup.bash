#!/bin/bash -e

name=run_2025-06-01_db_setup
rundir=../runs/$name

rm -rf $rundir
mkdir -p $rundir

date > $rundir/date_started.txt

rm -rf ../big_dbs

./setup_cath40.bash
./setup_scop40.bash
./setup_scop95.bash
./setup_scop40xs.bash
./setup_scop40_subsets.bash

git log \
	| head -n 20 \
	> $rundir/git_log.txt

cp -vr ../bash/ $rundir

date > $rundir/date_finished.txt
