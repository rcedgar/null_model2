#!/bin/bash -e

rm -f ../predict_FPEPQ/*

PF=0.5
##################################################################
xr=6:20
./predict_FPEPQ1.bash $xr $PF dali.scop40n4.scop40n4.scop40		dali.scop40.scop40.scop40	dali.scop40
./predict_FPEPQ1.bash $xr $PF dali.scop40sf4.scop40sf4.scop40	dali.scop40.scop40.scop40	dali.scop40	

PF=0.5
##################################################################
xr=0.1:0.2
./predict_FPEPQ1.bash $xr $PF reseek_fast_ts.scop40n4.scop40n4.scop40		reseek_fast_ts.scop40.scop40x8.scop40	reseek_ts.scop40
./predict_FPEPQ1.bash $xr $PF reseek_fast_ts.scop40sf4.scop40sf4.scop40		reseek_fast_ts.scop40.scop40x8.scop40	reseek_ts.scop40 

PF=1
##################################################################
xr=0.1:0.2
./predict_FPEPQ1.bash $xr $PF reseek_sensitive_ts.scop40n4.scop40n4.scop40		reseek_sensitive_ts.scop40.scop40x8.scop40	reseek_ts.scop40
./predict_FPEPQ1.bash $xr $PF reseek_sensitive_ts.scop40sf4.scop40sf4.scop40	reseek_sensitive_ts.scop40.scop40x8.scop40	reseek_ts.scop40 

##################################################################
xr=1:8
./predict_FPEPQ1.bash $xr $PF foldseek_default.scop40n4.scop40n4.scop40		foldseek_default.scop40.scop40x8.scop40	foldseek.scop40
./predict_FPEPQ1.bash $xr $PF foldseek_default.scop40sf4.scop40sf4.scop40	foldseek_default.scop40.scop40x8.scop40	foldseek.scop40 

##################################################################
xr=0.5:0.8
./predict_FPEPQ1.bash $xr $PF tm.scop40n4.scop40n4.scop40		tm.scop40.scop40.scop40		tm.scop40
./predict_FPEPQ1.bash $xr $PF tm.scop40sf4.scop40sf4.scop40		tm.scop40.scop40.scop40		tm.scop40

##################################################################
mkdir -p ../summary_pngs

cd ../predict_FPEPQ
montage -geometry 1000x1000 *.png ../summary_pngs/predict_FPEPQ.png
