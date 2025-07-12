#!/bin/bash -e

## tab separated first by field 2 then reverse field 1 numeric
## sort "-t     " -k2,2 -k1rg,1

pre=../big_data/hits/foldseek_default.scop40.afdb50
all=../big_data/hits/foldseek_exhaustive_scop40_vs_afdb.tsv

mkdir -p ../tmp
cd ../tmp

/bin/time -v -o sort_time.txt \
sort "-t	" -k1,1 -k3g,3 $all \
	| cut -f1,2,3 \
	> foldseek_sorted.tsv

head foldseek_sorted.tsv

/bin/time -v -o top_time.txt \
python ../py/topn_hits.py \
	--sorted_hits foldseek_sorted.tsv \
	--n 32 \
	> foldseek_top32.tsv

head foldseek_top32.tsv
ls -lh foldseek_top32.tsv

mkdir -p ../prefilter_top_hits

python ../py/top_hit_coverage.py \
	--tophits foldseek_top32.tsv \
	--fasthits $pre \
	| tee ../prefilter_top_hits/foldseek_scop40_afdb50.tsv
