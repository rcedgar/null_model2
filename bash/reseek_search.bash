#!/bin/bash -e

q=$1
db=$2

mkdir -p ../big_hits
mkdir -p ../log

if [ $q == scop40 -a $db == scop40 ] ; then
	mode=verysensitive
	hits=../big_hits/reseek_$mode.$q.$db
	../bin/reseek \
		-search ../big_dbs/reseek/$q.bca \
		-db ../big_dbs/reseek/$db.bca \
		-output $hits \
		-$mode \
		-columns query+target+evalue+dpscore+newts \
		-log ../log/reseek_$mode.$q.$db

	ls -lh $hits
fi

for mode in fast sensitive $vs
do
	hits=../big_hits/reseek_$mode.$q.$db
	../bin/reseek \
		-search ../big_dbs/reseek/$q.bca \
		-db ../big_dbs/reseek/$db.bca \
		-output $hits \
		-mints 0.05 \
		-$mode \
		-columns query+target+evalue+dpscore+newts \
		-log ../log/reseek_$mode.$q.$db

	ls -lh $hits
done
