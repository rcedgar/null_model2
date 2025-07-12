#!/bin/bash -e

outdir=../big_hits

fgrep -wFf ../big_dbs/reseek/afdb100k.labels \
	../big_hits/reseek_fast.scop40.afdb50 \
	| python ../py/cut.py 2,1,5 \
	| sed "-es/\/[a-z0-9.]*//" \
	> 	$outdir/reseek_fast_afdb_100ksubset.tsv
head	$outdir/reseek_fast_afdb_100ksubset.tsv
ls -lh 	$outdir/reseek_fast_afdb_100ksubset.tsv
