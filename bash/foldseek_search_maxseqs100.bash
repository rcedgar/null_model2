#!/bin/bash -e

qname=$1
dbname=$2

q=../big_dbs/foldseek/$qname/$qname
db=../big_dbs/foldseek/$dbname/$dbname

tmpdir=/tmp/foldseek_tmp
rm -rf $tmpdir

hits=../big_hits/foldseek_maxseqs100.$dbname
if [ -s $hits ] ; then
	echo =================================
	echo Found $hits
	echo =================================
	exit 0
fi

mkdir -p ../big_hits/

../bin/foldseek-v10 \
	easy-search \
	$q \
	$db \
	$hits \
	$tmpdir \
	--max-seqs 100 \
	-e 10 \
	--format-output query,target,evalue,bits,prob

rm -rf $tmpdir
