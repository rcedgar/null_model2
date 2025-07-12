#!/bin/bash -e

mkdir -p ../prefilter_sizes
cd ../prefilter_sizes

python ../py/prefilter_sizes_report.py \
	> prefilter_sizes_report.tsv

python ../py/columns.py \
	prefilter_sizes_report.tsv \
	| tee prefilter_sizes_report.txt

mkdir -p ../summary_pngs

cp prefilter_histogram.png ../summary_pngs
