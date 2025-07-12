#!/bin/bash -e

rm -rf ../predict_FPEPQsb
mkdir -p ../predict_FPEPQsb
cd ../predict_FPEPQsb

python ../py/predict_FPEPQb.py \
	--edf \
		tm.scop40n4.scop40n4.scop40 \
		tm.scop40n2.scop40n2.scop40 \
		tm.scop40.scop40.scop40 \
	--colors \
		0 \
		25 \
		50 \
	--labels \
		/4 \
		/2 \
		x1 \
	--title "TM-align" \
	--xlabel "TM score" \
	--xrange 0.4:0.8 \
	--plot tm.svg tm.png

python ../py/predict_FPEPQb.py \
	--edf \
		dali.scop40n4.scop40n4.scop40 \
		dali.scop40n2.scop40n2.scop40 \
		dali.scop40.scop40.scop40 \
	--colors \
		0 \
		25 \
		50 \
	--labels \
		/4 \
		/2 \
		x1 \
	--title "DALI" \
	--xlabel "Z score" \
	--xrange 2:23 \
	--plot dali.svg dali.png

python ../py/predict_FPEPQb.py \
	--edf \
		reseek_sensitive_ts.scop40n4.scop40n4.scop40 \
		reseek_sensitive_ts.scop40n2.scop40n2.scop40 \
		reseek_sensitive_ts.scop40.scop40.scop40 \
		reseek_sensitive_ts.scop40.scop40x4.scop40 \
		reseek_sensitive_ts.scop40.scop40x8.scop40 \
	--colors \
		0 \
		25 \
		50 \
		75 \
		100 \
	--labels \
		/4 \
		/2 \
		x1 \
		x4 \
		x8 \
	--title "Reseek (TS)" \
	--xlabel "TS" \
	--xrange 0.05:0.35 \
	--plot reseek.svg reseek.png

python ../py/predict_FPEPQb.py \
	--edf \
		foldseek_exhaustive.scop40n4.scop40n4.scop40 \
		foldseek_exhaustive.scop40n2.scop40n2.scop40 \
		foldseek_exhaustive.scop40.scop40.scop40 \
		foldseek_exhaustive.scop40.scop40x4.scop40 \
		foldseek_exhaustive.scop40.scop40x8.scop40 \
	--colors \
		0 \
		25 \
		50 \
		75 \
		100 \
	--labels \
		/4 \
		/2 \
		x1 \
		x4 \
		x8 \
	--title "Foldseek" \
	--xlabel "Reported E-value" \
	--xrange _1:12 \
	--evalues \
	--plot foldseek.svg foldseek.png

mkdir -p ../summary_pngs

montage -geometry 1000x1000 *.png \
	../summary_pngs/predict_FPEPQb.png
ls -l ../summary_pngs/predict_FPEPQb.png
