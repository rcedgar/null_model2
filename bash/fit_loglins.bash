#!/bin/bash -e

rm -rf ../fit_loglin
mkdir -p ../fit_loglin
cd ../fit_loglin

############################################
# TM-align
python ../py/loglin_fit_c_score_f.py \
	--edf ../edf/tm.scop40.scop40.scop40 \
	--output tm.scop40.tsv \
	--plot tm.scop40.svg,tm.scop40.png \
	--title "TM-align SCOP40" \
	--xlabel "TM score" \
	--textbox_x 0.5 \
	--textbox_y 1e-3 \
	--fitlo 0.55 \
	--fithi 0.62 \
	--yrange 1e-5:1e-2 \
	--xrange 0.4:0.65

python ../py/loglin_fit_c_score_f.py \
	--edf ../edf/tm.scop40.scop40.scop40c \
	--output tm.scop40c.tsv \
	--plot tm.scop40c.svg,tm.scop40c.png \
	--title "TM-align SCOP40c" \
	--xlabel "TM score" \
	--fitlo 0.55 \
	--fithi 0.62 \
	--textbox_x 0.5 \
	--textbox_y 1e-3 \
	--yrange 1e-5:1e-2 \
	--xrange 0.4:0.65

############################################
# DALI
############################################
python ../py/loglin_fit_c_score_f.py \
	--edf ../edf/dali.scop40.scop40.scop40 \
	--output dali.scop40.tsv \
	--plot dali.scop40.svg,dali.scop40.png \
	--title "DALI SCOP40" \
	--xlabel "Z score" \
	--textbox_y 1e-2 \
	--fitlo 10 \
	--fithi 19 \
	--yrange 1e-4:1e-1 \
	--xrange 5:23

python ../py/loglin_fit_c_score_f.py \
	--edf ../edf/dali.scop40.scop40.scop40c \
	--output dali.scop40c.tsv \
	--plot dali.scop40c.svg,dali.scop40c.png \
	--title "DALI SCOP40c" \
	--xlabel "Z score" \
	--textbox_y 1e-2 \
	--fitlo 10 \
	--fithi 14 \
	--yrange 1e-4:1e-1 \
	--xrange 5:23

############################################
# Foldseek
############################################
python ../py/loglin_fit_c_score_f.py \
	--edf ../edf/foldseek_exhaustive.scop40.scop40.scop40 \
	--output foldseek.scop40.tsv \
	--plot foldseek.scop40.svg,foldseek.scop40.png \
	--title "Foldseek SCOP40" \
	-x-log10\(E\) \
	--fitlo 2 \
	--fithi 6 \
	--xrange _1:8

python ../py/loglin_fit_c_score_f.py \
	--edf ../edf/foldseek_exhaustive.scop40.scop40.scop40c \
	--output foldseek.scop40c.tsv \
	--plot foldseek.scop40c.svg,foldseek.scop40c.png \
	--title "Foldseek SCOP40c" \
	-x-log10\(E\) \
	--fitlo 1 \
	--fithi 4 \
	--xrange _1:8

############################################
# Reseek E-value
############################################
python ../py/loglin_fit_c_score_f.py \
	--edf ../edf/reseek_sensitive_evalue.scop40.scop40.scop40 \
	--output reseek_evalue.scop40.tsv \
	--plot reseek_evalue.scop40.svg,reseek_evalue.scop40.png \
	--title "Reseek SCOP40" \
	-x-log10\(E\) \
	--fitlo 1 \
	--fithi 2.5 \
	--xrange _1:4

python ../py/loglin_fit_c_score_f.py \
	--edf ../edf/reseek_sensitive_evalue.scop40.scop40.scop40c \
	--output reseek_evalue.scop40c.tsv \
	--plot reseek_evalue.scop40c.svg,reseek_evalue.scop40c.png \
	--title "Reseek SCOP40c" \
	-x-log10\(E\) \
	--fitlo 1 \
	--fithi 2.5 \
	--xrange _1:4

############################################
# Reseek TS
############################################
python ../py/loglin_fit_c_score_f.py \
	--edf ../edf/reseek_sensitive_ts.scop40.scop40.scop40 \
	--output reseek_ts.scop40.tsv \
	--plot reseek_ts.scop40.svg,reseek_ts.scop40.png \
	--title "Reseek SCOP40" \
	--xlabel TS \
	--fitlo 0.15 \
	--fithi 0.25 \
	--xrange 0.05:0.3

python ../py/loglin_fit_c_score_f.py \
	--edf ../edf/reseek_sensitive_ts.scop40.scop40.scop40c \
	--output reseek_ts.scop40c.tsv \
	--plot reseek_ts.scop40c.svg,reseek_ts.scop40c.png \
	--title "Reseek SCOP40c" \
	--xlabel TS \
	--fitlo 0.125 \
	--fithi 0.2 \
	--xrange 0.05:0.3

mkdir -p ../summary_pngs

montage -geometry 1000x1000 *.png \
	../summary_pngs/fit_loglins.png
