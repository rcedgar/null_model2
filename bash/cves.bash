#!/bin/bash -e

python ../py/plot_cves_scop40_algos.py scop40
python ../py/plot_cves_scop40_algos.py scop40c

cd ../cves
mkdir -p ../summary_pngs
montage -geometry 1000x1000 *.png ../summary_pngs/cves.png
