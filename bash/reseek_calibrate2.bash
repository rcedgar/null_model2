#!/bin/bash -e

rm -rf ../reseek_calibrate2
mkdir -p ../reseek_calibrate2
cd ../reseek_calibrate2

python ../py/reseek_calibrate_v2.py

python ../py/columns.py evalue.tsv \
	> evalue.txt

mkdir -p ../summary_pngs

montage -geometry 1000x1000 *.png \
	../summary_pngs/reseek_calibrate2.png
