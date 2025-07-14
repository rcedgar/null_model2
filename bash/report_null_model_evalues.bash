#!/bin/bash -e

cd ../report_null_model_evalues

python ../py/report_null_model_evalues.py \
	--input dali.tsv \
	--score Z \
	--dbsize 11211 \
	--column 3 \
	> tm_scop40c.tsv

python ../py/report_null_model_evalues.py \
	--input dali.tsv \
	--score Z \
	--dbsize 11211 \
	--column 3 \
	--scop40 \
	> tm_scop40.tsv

python ../py/report_null_model_evalues.py \
	--input tm.tsv \
	--score TM \
	--dbsize 11211 \
	--column 3 \
	> tm_scop40c.tsv

python ../py/report_null_model_evalues.py \
	--input tm.tsv \
	--score TM \
	--dbsize 11211 \
	--column 3 \
	--scop40 \
	> tm_scop40.tsv

python ../py/report_null_model_evalues.py \
	--input foldseek.tsv \
	--score E \
	--dbsize 11211 \
	--column 3 \
	> foldseek_scop40c.tsv

python ../py/report_null_model_evalues.py \
	--input foldseek.tsv \
	--score E \
	--dbsize 11211 \
	--column 3 \
	--scop40 \
	> foldseek_scop40.tsv
