#!/bin/bash -e

rm -rf ../fit_loglin_P
mkdir -p ../fit_loglin_P
cd ../fit_loglin_P

############################################
# Foldseek
############################################
python ../py/loglin_fit_c_score_f.py \
	--edf ../edf/foldseek_exhaustive.scop40.scop40.scop40 \
	--prob \
	--output foldseek.scop40.tsv \
	--plot foldseek.scop40.svg,foldseek.scop40.png \
	--title "Foldseek SCOP40" \
	-x-log10\(E\) \
	--fitlo 2 \
	--fithi 4 \
	--textbox_y 1e-2 \
	--yrange 1e-4:0.1 \
	--xrange 0:6

python ../py/loglin_fit_c_score_f.py \
	--edf ../edf/foldseek_exhaustive.scop40.scop40.scop40c \
	--prob \
	--output foldseek.scop40c.tsv \
	--plot foldseek.scop40c.svg,foldseek.scop40c.png \
	--title "Foldseek SCOP40c" \
	--textbox_y 1e-2 \
	-x-log10\(E\) \
	--fitlo 0.5 \
	--fithi 3 \
	--yrange 1e-4:0.1 \
	--xrange 0:4

############################################
# Reseek TS
############################################
python ../py/loglin_fit_c_score_f.py \
	--edf ../edf/reseek_sensitive_ts.scop40.scop40.scop40 \
	--prob \
	--output reseek_ts.scop40.tsv \
	--plot reseek_ts.scop40.svg,reseek_ts.scop40.png \
	--title "Reseek SCOP40" \
	--xlabel TS \
	--fitlo 0.10 \
	--fithi 0.20 \
	--xrange 0.05:0.25

python ../py/loglin_fit_c_score_f.py \
	--edf ../edf/reseek_sensitive_ts.scop40.scop40.scop40c \
	--prob \
	--output reseek_ts.scop40c.tsv \
	--plot reseek_ts.scop40c.svg,reseek_ts.scop40c.png \
	--title "Reseek SCOP40" \
	--xlabel TS \
	--fitlo 0.1 \
	--fithi 0.2 \
	--xrange 0.05:0.25

mkdir -p ../summary_pngs

montage -geometry 1000x1000 *.png \
	../summary_pngs/fit_loglins_P.png
