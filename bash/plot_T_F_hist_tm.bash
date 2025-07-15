#!/bin/bash -e

mkdir -p ../T_F_hist
cd ../T_F_hist

python ../py/T_F_hist.py \
	--edf ../edf/tm.scop40.scop40.scop40 \
	--plot tm.svg

python ../py/T_F_hist.py \
	--edf ../edf/tm.scop40.scop40.scop40 \
	--ymax 1e5 \
	--plot tm_zoomed.svg
