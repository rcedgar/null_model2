#!/bin/bash -e

d=../bayes_evalue_table
rm -rf $d
mkdir -p $d
python ../py/bayes_evalue_table.py \
	| tee ../bayes_evalue_table/bayes_evalue_table.txt

