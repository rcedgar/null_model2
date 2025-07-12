#!/bin/bash -e

mkdir -p ../top_fps

python ../py/top_fps.py \
	--hits ../big_hits/dali.scop40 \
	--edf ../edf/dali.scop40 \
	> ../top_fps/dali.scop40

python ../py/top_fps.py \
	--hits ../big_hits/foldseek.scop40 \
	--edf ../edf/foldseek.scop40 \
	--evalues \
	> ../top_fps/foldseek.scop40

python ../py/top_fps.py \
	--hits ../big_hits/reseek.scop40 \
	--edf ../edf/reseek.scop40 \
	--evalues \
	> ../top_fps/reseek.scop40

python ../py/top_fps.py \
	--hits ../big_hits/tm.scop40 \
	--edf ../edf/tm.scop40 \
	> ../top_fps/tm.scop40

cd ../top_fps

python ../py/top_fps_report.py \
	top_fps_report_scop40.txt \
	ex_scop40.txt \
	scop40 \
	dali tm foldseek reseek
