#!/bin/bash -e

# [8719e82]+1 Prepping run_2025-05-28_end_to_end_with_predict_EPQs.bash

################################
# MUST conda activate null_model
################################

name=2025-05-28_end_to_end_with_predict_EPQs
rundir=../runs/$name

rm -rf $rundir
mkdir -p $rundir

date >> $rundir/date.txt

######################################################
cd ../big_hits
rm -rf `ls | fgrep -v tm.scop40 | fgrep -v dali.scop40`
cd ../bash

rm -rf ../edf
rm -rf ../cves
rm -rf ../plots
rm -rf ../big_dbs
rm -rf ../fit_loglins
rm -rf ../fit_gumbels
rm -rf ../predict_FPEPQ
rm -rf ../predict_P_F_score
######################################################

## ./download_dali_and_tm_hits.bash

./setup_cath40.bash
./setup_scop40.bash
./setup_scop95.bash
./setup_scop40xs.bash

./reseek_search.bash cath40
./reseek_search.bash scop40
./reseek_search.bash scop95
./reseek_search_xs.bash
./reseek_fast_search_scop40.bash
./reseek_fast_search_xs.bash

./foldseek_search.bash cath40
./foldseek_search.bash scop40
./foldseek_search.bash scop95
./foldseek_search_xs.bash
./foldseek_search_maxseqs.bash

./edfs.bash
./edf_avgs.bash
./c_false_plots.bash # should have included ./p_false_plots.bash here
./predict_FPEPQs.bash
./predict_P_F_scores.bash

## python ../py/plot_cves_scop40_algos.py scop40
## python ../py/plot_cves_scop40_algos.py scop40c
./cves.bash

git log \
	| head -n 20 \
	> $rundir/git_log.txt

cp -vr ../edf $rundir
cp -vr ../cves $rundir
cp -vr ../plots $rundir
cp -vr ../fit_loglin $rundir
cp -vr ../fit_gumbel $rundir
cp -vr ../predict_FPEPQ $rundir
cp -vr ../predict_P_F_score $rundir
cp -vr ../bash/* $rundir
cp -vr ../py/* $rundir

date >> $rundir/date.txt

# ./sync_to_s3.bash
