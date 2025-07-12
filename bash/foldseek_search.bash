#!/bin/bash -e

qname=$1
dbname=$2

q=../big_dbs/foldseek/$qname/$qname
db=../big_dbs/foldseek/$dbname/$dbname

tmpdir=/tmp/tmp_foldseek
rm -rf $tmpdir

mkdir -p ../big_hits/

hits=../big_hits/foldseek_default.${qname}.$dbname
../bin/foldseek-v10 \
	easy-search \
	$q \
	$db \
	$hits \
	$tmpdir \
	-e 10 \
	--format-output query,target,evalue,bits,prob

rm -rf $tmpdir


hits=../big_hits/foldseek_exhaustive.${qname}.$dbname
../bin/foldseek-v10 \
	easy-search \
	$q \
	$db \
	$hits \
	$tmpdir \
	-e 10 \
	--exhaustive-search 1 \
	--format-output query,target,evalue,bits,prob

rm -rf $tmpdir
