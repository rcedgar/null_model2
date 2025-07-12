#!/bin/bash -e

# [0835507] 2025-05-11_c_false_plots_linscale
# [0835507]+1 has runs/2025-05-11_c_false_plots_linscale

name=2025-05-08_c_false_plots_linscale
rundir=../runs/$name
rm -rf $rundir
mkdir -p $rundir

./plot_C_F_score_selected_linscale.bash
./plot_C_score_F_selected_linscale.bash

mkdir -p $rundir/plot
mkdir -p $rundir/edf

cp -v ../plots/C_F_score_selected_linscale.svg $rundir/plot
cp -v ../plots/C_score_F_selected_linscale.svg $rundir/plot

cp -v ../edf/* $rundir/edf
