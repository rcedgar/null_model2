#!/bin/bash -e

name=`echo $0 | sed "-es/.*run_//" | sed "-es/\.bash//"`
rundir=../runs/$name

rm -rf $rundir
mkdir -p $rundir

uname -a > $rundir/date.txt
echo start `date` >> $rundir/date.txt

./foldseek_and_reseek_searches.bash

git log \
	| head -n 20 \
	> $rundir/git_log.txt

ls -ltrh ../big_hits > $rundir/big_hits.ls

mkdir -p $rundir/bash
cp -v *search* $rundir/bash

echo done `date` >> $rundir/date.txt
