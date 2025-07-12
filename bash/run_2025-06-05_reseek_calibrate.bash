#!/bin/bash -e

name=`echo $0 | sed "-es/.*run_//" | sed "-es/\.bash//"`
rundir=../runs/$name

rm -rf $rundir
mkdir -p $rundir

date > $rundir/date_started.txt

for mode in fast sensitive verysensitive
do
	$src/reseek/github_releases/reseek-v2.5-linux-x86 \
		-search ../big_dbs/reseek/$q.bca \
		-db ../big_dbs/reseek/$db.bca \
		-nochainchar \
		-output $hits \
		-dbsize 11211 \
		-$mode  \
		-evalue 10 \
		-columns query+target+evalue+dpscore+newts \
		-log ../log/$q.$db
done

date > $rundir/date_finished.txt
