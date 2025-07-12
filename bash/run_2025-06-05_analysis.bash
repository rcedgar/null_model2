#!/bin/bash -e

########################################
# MUST create and activate null_model
# See bash/create_conda_environment.bash 
########################################

name=`echo $0 | sed "-es/.*run_//" | sed "-es/\.bash//"`
rundir=../runs/$name

rm -rf $rundir
mkdir -p $rundir

date > $rundir/date_begin.txt

results_dirs=
for dir in \
	edf \
	cves \
	fit_loglin \
	predict_FPEPQ \
	prefilter_sizes \
	C_score_F_same \
	P_F_score_varies
do
	results_dirs="$results_dirs "$dir
done

for dir in $results_dirs
do
	rm -rf ../$dir
done

./edfs.bash
./edfs_other.bash
./edfs_reseek_sizes.bash
./edfs_foldseek_sizes.bash
./prefilter_sizes_report.bash
./cves.bash
./fit_loglins.bash
./predict_FPEPQs.bash
./C_score_F_same.bash
./P_F_score_varies.bash

git log \
	| head -n 20 \
	> $rundir/git_log.txt

cp -vr ../plot_specs/ $rundir
cp -vr ../bash/ $rundir
cp -vr ../py/ $rundir

for dir in $results_dirs
do
	cp -vr ../$dir $rundir
done

date > $rundir/date_end.txt
