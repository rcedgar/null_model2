#!/bin/bash -e

if [ -s ../big_hits/tm.scop40 -a -s ../big_hits/dali.scop40 ] ; then
	echo Skipping tm and dali download
	exit 0
fi

if [ ! -s ../tmp_download/scop.benchmark.result.tar.gz ] ; then
	mkdir -p ../tmp_download
	cd ../tmp_download
	wget https://wwwuser.gwdguser.de/~compbiol/foldseek/scop.benchmark.result.tar.gz
fi

cd ../tmp_download
tar -zxvf scop.benchmark.result.tar.gz

mkdir -p ../big_hits

if [ ! -s ../big_hits/tm.scop40 ] ; then
	cp ../tmp_download/TMalign.txt ../big_hits/tm.scop40
fi

if [ ! -s ../big_hits/dali.scop40 ] ; then
	cp ../tmp_download/dali.txt ../big_hits/dali.scop40
fi
