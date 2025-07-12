#!/bin/bash -e

mode=$1
ref=$2
q=$3
db=$4
dbdupes=$5
divn=$6
divsf=$7

if [ x$divsf == x ] ; then
	echo $0: Missing arg
	exit 1
fi

mkdir -p ../edf

lookup=../data/$ref.lookup
hits=../big_hits/foldseek_$mode.$q.$db

q2=$q
db2=$db

opts=
if [ $divn != 1 ] ; then
	opts="$opts --subn $divn"
	q2=${q}n$divn
	db2=$q2
elif [ $divsf != 1 ] ; then
	opts="$opts --subsf $divsf"
	q2=${q}sf$divsf
	db2=$q2
elif [ $dbdupes != 1 ] ; then
	opts="$opts --dbdupes $dbdupes"
fi

if [ $ref == none ] ; then
	python ../py/edf_noref.py \
		--hits $hits \
		--field 3 \
		--evalues \
		--minevalue 1e-60 \
		> ../edf/foldseek_${mode}.$q2.$db2.$ref
else
	python ../py/empdist.py \
		--hits $hits \
		--lookup $lookup \
		--fields 1,2,3 \
		--dbdupes $dbdupes \
		--minevalue 1e-20 \
		--maxevalue 10 \
		--evalues \
		$opts \
		--output ../edf/foldseek_${mode}.$q2.$db2.$ref
fi
