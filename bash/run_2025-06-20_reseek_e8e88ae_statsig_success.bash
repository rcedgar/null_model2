#!/bin/bash -e

name=`echo $0 | sed "-es/.*run_//" | sed "-es/\.bash//"`
rundir=../runs/$name

rm -rf $rundir
mkdir -p $rundir

uname -a > $rundir/date.txt
echo start `date` >> $rundir/date.txt

mkdir -p ../statsig_success
cd ../statsig_success

reseek=../bin/reseek \

for mode in fast sensitive
do
	$reseek \
		-search ../big_dbs/reseek/scop40.bca \
		-db ../big_dbs/reseek/scop40.bca \
		-output ../big_hits/reseek_e8e88ae_$mode.tsv \
		-columns query+target+evalue+dpscore+newts \
		-log $mode.log \
		-$mode

	python ../py/empdist.py \
		--hits ../big_hits/reseek_e8e88ae_$mode.tsv \
		--fields 1,2,3 \
		--evalues \
		--qname scop40 \
		--dbname scop40 \
		--output $mode.edf		
done

python ../py/plot_evalue_vs_epq.py \
	--edfs \
		fast.edf \
		sensitive.edf \
	--labels fast sensitive \
	--xrange 1e-3:10 \
	--plot evalue_vs_epq.svg

cp -vr . $rundir

echo done `date` >> $rundir/date.txt
