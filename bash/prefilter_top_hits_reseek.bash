#!/bin/bash -e

## tab separated first by field 2 then reverse field 1 numeric
## sort "-t     " -k2,2 -k1rg,1

pre=../big_data/hits/reseek_fast.scop40.afdb50
all=../big_data/hits/reseek_sensitive_scop40_vs_afdb.tsv

mkdir -p ../prefilter_top_hits
mkdir -p ../tmp
cd ../tmp

/bin/time -v -o sort_time.txt \
sort "-t	" -k1,1 -k3g,3 $all \
	| cut -f1,2,3 \
	> reseek_sorted.tsv

head reseek_sorted.tsv

/bin/time -v -o top_time.txt \
python ../py/topn_hits.py \
	--sorted_hits reseek_sorted.tsv \
	--n 32 \
	> reseek_top32.tsv

head reseek_top32.tsv
ls -lh reseek_top32.tsv

python ../py/top_hit_coverage.py \
	--tophits reseek_top32.tsv \
	--fasthits $pre \
    --qfield 2 \
    --tfield 1 \
	| tee ../prefilter_top_hits/reseek_scop40_afdb50.tsv
