#!/bin/bash -e

q=$1
db=$2

mkdir -p ../big_hits
mkdir -p ../log

name=reseek_rsbsize100.${db}
hits=../big_hits/$name

if [ -s $hits ] ; then
	echo =======================
	echo Found $hits
	echo =======================
	exit 0
fi

reseek=../bin/reseek_v2.5_with_rsb_size_option

$reseek \
	-search ../big_dbs/reseek/$q.bca \
	-db ../big_dbs/reseek/${db}.bca \
	-nochainchar \
	-output $hits \
	-dbsize 11211 \
	-fast \
	-rsb_size 100 \
	-evalue 10 \
	-columns query+target+evalue+dpscore+newts \
	-log ../log/$name

ls -lh $hits
