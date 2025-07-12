#!/bin/bash -e

rm -rf ../reseek_calibrate
mkdir -p ../reseek_calibrate
cd ../reseek_calibrate

python ../py/reseek_calibrate.py

mkdir -p ../summary_pngs

montage -geometry 1000x1000 *.png \
	../summary_pngs/reseek_calibrate.png
