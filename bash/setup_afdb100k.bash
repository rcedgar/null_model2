#!/bin/bash -e

rm -rf ../big_dbs/afdb100k/
rm -rf ../big_dbs/reseek/afdb100k*
rm -rf ../big_dbs/foldseek/afdb100k*

mkdir -p ../big_dbs/afdb100k/pdb_caonly
mkdir -p ../big_dbs/reseek

afdb50_bca=$c/int/afdb/out/afdb50.bca

../bin/reseek \
    -convert $afdb50_bca \
    -sample_step 537 \
	-randseed 1 \
	-delete_chaina \
    -bca ../big_dbs/reseek/afdb100k.bca \
    -cal ../big_dbs/reseek/afdb100k.cal \
	-pdbcaoutdir ../big_dbs/afdb100k/pdb_caonly

grep "^>" ../big_dbs/reseek/afdb100k.cal \
	| tr -d '>' \
	> ../big_dbs/reseek/afdb100k.labels

cat ../big_dbs/reseek/afdb100k.labels \
	| sed "-es/_v4/_v4A/" \
	> ../big_dbs/reseek/afdb100k.labelsa

cat ../big_dbs/reseek/afdb100k.labels \
	| wc -l \
	> ../big_dbs/reseek/afdb100k.size

dbdir=../big_dbs/foldseek/afdb100k
mkdir -p $dbdir

foldseek-v10 \
    createdb \
    ../big_dbs/afdb100k/pdb_caonly \
    $dbdir/afdb100k
