#!/bin/bash -e

# these scripts use ../tmp
./prefilter_top_hits_foldseek.bash
./prefilter_top_hits_reseek.bash

mkdir -p ../prefilter_top_hits

# svg ../prefilter_top_hits, ../summary_pngs
python ../py/prefilter_top_hit_figure.py
