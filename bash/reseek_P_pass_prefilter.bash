#!/bin/bash -e

###########################
# WARNING
###########################
rm -rf ../P_prefilter
###########################

mkdir -p ../P_prefilter
cd ../P_prefilter

#################################################
# P(pass prefilter | TS)
#################################################
python ../py/reseek_P_pass_prefilter_afdb.py \
	> afdb50.tsv

python ../py/reseek_P_pass_prefilter_edfs.py \
	scop40 scop40 \
	> scop40.tsv

python ../py/reseek_P_pass_prefilter_edfs.py \
	scop40 scop40c \
	> scop40c.tsv

python ../py/reseek_P_pass_prefilter_edfs.py \
	bfvd none \
	> bfvd.tsv

python ../py/reseek_P_pass_prefilter_edfs.py \
	pdb none \
	> pdb.tsv

#################################################
# CDF
#################################################
python ../py/reseek_P_pass_prefilter2_afdb.py scop40 \
	> afdb50_cdf.tsv

python ../py/reseek_P_pass_prefilter2_afdb.py scop40c \
	> afdb50_c_cdf.tsv

python ../py/reseek_P_pass_prefilter2.py scop40.tsv scop40 \
	> scop40_cdf.tsv

python ../py/reseek_P_pass_prefilter2.py scop40c.tsv scop40c \
	> scop40_c_cdf.tsv

python ../py/reseek_P_pass_prefilter2.py bfvd.tsv scop40 \
	> bfvd_cdf.tsv

python ../py/reseek_P_pass_prefilter2.py bfvd.tsv scop40c \
	> bfvd_c_cdf.tsv

python ../py/reseek_P_pass_prefilter2.py pdb.tsv scop40 \
	> pdb_cdf.tsv

python ../py/reseek_P_pass_prefilter2.py pdb.tsv scop40c \
	> pdb_c_cdf.tsv

python ../py/loglin_fit_hist.py \
	--hist scop40_cdf.tsv \
	--header \
	--scorefield 1 \
	--yfield 4 \
	--fitlo 0.15 \
	--fithi 0.3 \
	--xlabel "TS" \
	--ylabel "CDF" \
	--title SCOP40 \
	--textbox_y 1e-2 \
	--xrange 0.05:0.4 \
	--yrange 1e-5:0.1 \
	--output scop40_fit.tsv \
	--plot scop40.svg scop40.png

python ../py/loglin_fit_hist.py \
	--hist scop40_c_cdf.tsv \
	--header \
	--scorefield 1 \
	--yfield 4 \
	--fitlo 0.15 \
	--fithi 0.25 \
	--xlabel "TS" \
	--ylabel "CDF" \
	--title SCOP40c \
	--textbox_y 6e-3 \
	--xrange 0.05:0.3 \
	--yrange 1e-5:0.1 \
	--output scop40_c_fit.tsv \
	--plot scop40c.svg scop40c.png

python ../py/loglin_fit_hist.py \
	--hist afdb50_cdf.tsv \
	--header \
	--scorefield 1 \
	--yfield 4 \
	--fitlo 0.15 \
	--fithi 0.3 \
	--xlabel "TS" \
	--ylabel "CDF" \
	--title AFDB \
	--textbox_x 0.3 \
	--textbox_y 2e-4 \
	--xrange 0.1:0.4 \
	--yrange 1e-6:0.001 \
	--output afdb50_fit.tsv \
	--plot afdb50.png afdb50.svg

python ../py/loglin_fit_hist.py \
	--hist afdb50_c_cdf.tsv \
	--header \
	--scorefield 1 \
	--yfield 4 \
	--fitlo 0.15 \
	--fithi 0.25 \
	--xlabel "TS" \
	--ylabel "CDF" \
	--title AFDBc \
	--textbox_y 2e-4 \
	--xrange 0.05:0.4 \
	--yrange 1e-6:0.001 \
	--output afdb50_c_fit.tsv \
	--plot afdb50c.png afdb50c.svg

python ../py/loglin_fit_hist.py \
	--hist bfvd_cdf.tsv \
	--header \
	--scorefield 1 \
	--yfield 4 \
	--fitlo 0.2 \
	--fithi 0.3 \
	--xlabel "TS" \
	--ylabel "CDF" \
	--title BFVD \
	--textbox_x 0.3 \
	--textbox_y 1e-3 \
	--xrange 0.1:0.5 \
	--yrange 1e-5:0.01 \
	--output bfvd_fit.tsv \
	--plot bfvd.svg bfvd.png

python ../py/loglin_fit_hist.py \
	--hist bfvd_c_cdf.tsv \
	--header \
	--scorefield 1 \
	--yfield 4 \
	--fitlo 0.175 \
	--fithi 0.25 \
	--xlabel "TS" \
	--ylabel "CDF" \
	--title BFVDc \
	--textbox_x 0.175 \
	--textbox_y 5e-5 \
	--xrange 0.1:0.3 \
	--yrange 1e-5:0.01 \
	--output bfvd_c_fit.tsv \
	--plot bfvdc.svg bfvdc.png

python ../py/loglin_fit_hist.py \
	--hist pdb_cdf.tsv \
	--header \
	--scorefield 1 \
	--yfield 4 \
	--fitlo 0.2 \
	--fithi 0.3 \
	--xlabel "TS" \
	--ylabel "CDF" \
	--title PDB \
	--textbox_x 0.3 \
	--textbox_y 1e-3 \
	--xrange 0.1:0.4 \
	--yrange 1e-5:0.005 \
	--output pdb_fit.tsv \
	--plot pdb.svg pdb.png

python ../py/loglin_fit_hist.py \
	--hist pdb_c_cdf.tsv \
	--header \
	--scorefield 1 \
	--yfield 4 \
	--fitlo 0.2 \
	--fithi 0.25 \
	--xlabel "TS" \
	--ylabel "CDF" \
	--title PDBc \
	--textbox_y 1e-3 \
	--xrange 0.1:0.3 \
	--yrange 1e-5:0.005 \
	--output pdb_c_fit.tsv \
	--plot pdbc.svg pdbc.png

mkdir -p ../summary_pngs

montage -geometry 1000x1000 *.png \
	../summary_pngs/P_pass_prefilter.png
