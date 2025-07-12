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
hits=../big_hits/tm.scop40

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

python ../py/empdist.py \
	--hits ../big_hits/tm.scop40 \
	--lookup $lookup \
	--fields 1,2,3 \
	--dbdupes $dbdupes \
	--minscore 0 \
	--maxscore 1 \
	--seed 1 \
	$opts \
	--output ../edf/tm.$q2.$db2.$ref
