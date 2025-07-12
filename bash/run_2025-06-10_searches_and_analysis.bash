#!/bin/bash -e

########################################
# MUST create and activate null_model
# See bash/create_conda_environment.bash 
########################################

name=`echo $0 | sed "-es/.*run_//" | sed "-es/\.bash//"`
rundir=../runs/$name

rm -rf $rundir
mkdir -p $rundir

uname -a > $rundir/date.txt
echo start `date` >> $rundir/date.txt

results_dirs=
for dir in \
	edf \
	cves \
	fit_loglin \
	fit_gumbel \
	predict_FPEPQ \
	prefilter_sizes \
	C_score_F \
	P_T_score \
	evalue_vs_epq \
	summary_pngs
do
	results_dirs="$results_dirs "$dir
done

for dir in $results_dirs
do
	rm -rf ../$dir
done

./foldseek_and_reseek_searches.bash
./run_blastp.bash
./edfs.bash
./edf_blastp.bash
./evalue_vs_epq.bash
./prefilter_sizes_report.bash
./cves.bash
./smith_waterman_3di_fit_gumbel.bash
./reseekdp_fit_gumbel.bash
./fit_gumbels_summary_png.bash
./fit_loglins.bash
./predict_FPEPQs.bash
./C_score_F.bash
./P_T_score.bash

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

echo done `date` >> $rundir/date.txt
