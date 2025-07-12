#!/bin/bash -e

mkdir -p ../top_fps

python ../py/top_fps.py \
	--hits ../big_hits/dali.scop40 \
	--edf ../edf/dali.scop40c \
	--lookup ../data/scop40c.lookup \
	> ../top_fps/dali.scop40c

python ../py/top_fps.py \
	--hits ../big_hits/foldseek.scop40 \
	--edf ../edf/foldseek.scop40c \
	--lookup ../data/scop40c.lookup \
	--evalues \
	> ../top_fps/foldseek.scop40c

python ../py/top_fps.py \
	--hits ../big_hits/reseek.scop40 \
	--edf ../edf/reseek.scop40c \
	--lookup ../data/scop40c.lookup \
	--evalues \
	> ../top_fps/reseek.scop40c

python ../py/top_fps.py \
	--hits ../big_hits/tm.scop40 \
	--edf ../edf/tm.scop40c \
	--lookup ../data/scop40c.lookup \
	> ../top_fps/tm.scop40c

cd ../top_fps

python ../py/top_fps_report.py \
	top_fps_report_scop40c.txt \
	ex_scop40c.txt \
	scop40c \
	dali tm foldseek reseek
