#!/bin/bash -e

mkdir -p ../evalue_by_interp2
cd ../evalue_by_interp2

python ../py/evalue_by_interp2.py \
	--ref_dbsize 11211 \
	--edf_ref ../edf/reseek.scop40 \
	--edf_target ../edf/reseek.scop40 \
	--lo 1e-5 \
	--hi 11 \
	--m -0.8248 \
	--c -0.6823 \
	> reseek_scop40_scop40

python ../py/evalue_by_interp2.py \
	--ref_dbsize 11211 \
	--edf_ref ../edf/reseek.scop40c \
	--edf_target ../edf/reseek.scop40c \
	--lo 1e-5 \
	--hi 11 \
	--m -0.9962 \
	--c -0.9978 \
	> reseek_scop40c_scop40c

python ../py/evalue_by_interp2.py \
	--ref_dbsize 11211 \
	--edf_ref ../edf/foldseek.scop40 \
	--edf_target ../edf/foldseek.scop40 \
	--lo 1e-20 \
	--hi 11 \
	--m -0.1943 \
	--c 0.08799 \
	> foldseek_scop40_scop40

python ../py/evalue_by_interp2.py \
	--ref_dbsize 11211 \
	--edf_ref ../edf/foldseek.scop40c \
	--edf_target ../edf/foldseek.scop40c \
	--lo 1e-20 \
	--hi 11 \
	--m -0.4414 \
	--c 0.534 \
	> foldseek_scop40c_scop40c

python ../py/evalue_by_interp2.py \
	--ref_dbsize 11211 \
	--edf_ref ../edf/reseek.scop40 \
	--edf_target ../edf/reseek_fast.scop40_afdb50 \
	--lo 1e-5 \
	--hi 11 \
	--m -0.8248 \
	--c -0.6823 \
	> reseek_scop40_afdb50

python ../py/evalue_by_interp2.py \
	--ref_dbsize 8340 \
	--edf_ref ../edf/reseek.scop40c \
	--edf_target ../edf/reseek_fast.scop40_afdb50 \
	--lo 1e-5 \
	--hi 11 \
	--m -0.9962 \
	--c -0.9978 \
	> reseek_scop40c_afdb50

python ../py/evalue_by_interp2.py \
	--ref_dbsize 11211 \
	--edf_ref ../edf/foldseek.scop40 \
	--edf_target ../edf/foldseek.scop40_afdb50 \
	--lo 1e-20 \
	--hi 11 \
	--m -0.1943 \
	--c 0.08799 \
	> foldseek_scop40_afdb50

python ../py/evalue_by_interp2.py \
	--ref_dbsize 11211 \
	--edf_ref ../edf/foldseek.scop40c \
	--edf_target ../edf/foldseek.scop40_afdb50 \
	--hi 11 \
	--lo 1e-20 \
	--m -0.4414 \
	--c 0.534 \
	> foldseek_scop40c_afdb50

mkdir -p ../evalue_by_interp2_txt
for x in *
do
	echo $x
	grep -v '^#' $x | python ../py/columns.py \
		> ../evalue_by_interp2_txt/$x
done
