#!/bin/bash -e

#########################################
# WARNING WARNING WARNING WARNING WARNING
#########################################
rm -rf ../big_hits
#########################################

name=`echo $0 | sed "-es/.*run_//" | sed "-es/\.bash//"`
rundir=../runs/$name

rm -rf $rundir
mkdir -p $rundir

uname -a > $rundir/date.txt
echo start `date` >> $rundir/date.txt

../bin/reseek --version > $rundir/reseek_version.txt

./foldseek_and_reseek_searches.bash
./link_big_hits.bash

git log \
	| head -n 20 \
	> $rundir/git_log.txt

ls -lh ../big_hits >> $rundir/big_hits.ls

echo done `date` >> $rundir/date.txt
