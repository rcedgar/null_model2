#!/bin/bash -e

X=$1

if [ x$X == x ] ; then
	echo $0: Missing arg
	exit 1
fi

outdir=../big_dbs/reseek
mkdir -p $outdir

input_cal=../big_data/dbs/scop40.fs.cal
output_cal=$outdir/scop40x$X.cal
output_bca=$outdir/scop40x$X.bca

if [ ! -s $output_cal -o ! -s $output_bca ] ; then
	cat $input_cal \
		> $output_cal

	for i in `seq 1 $((X-1))`
	do
		echo i=$i
		cat $input_cal \
			| sed "-es/^>/>DUPE${i}_/" \
			>> $output_cal
	done

	reseek \
		-convert $output_cal \
		-bca $output_bca
fi

dbdir=../big_dbs/foldseek/scop40x$X/
mkdir -p $dbdir

reseek \
	-create_foldseekdb ../big_data/scop40.fs.bca \
	-3di ../big_data/scop40.3di.fa \
	-n $X \
	-output $dbdir/scop40x$X

cd ../data
cp -v scop40.lookup scop40x$X.lookup
