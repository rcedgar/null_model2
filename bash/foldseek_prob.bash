#!/bin/bash -e

d=../foldseek_prob

rm -rf $d
mkdir -p $d
cd $d

python ../py/foldseek_prob.py

python ../py/columns.py summary.tsv
