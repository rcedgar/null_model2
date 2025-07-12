#!/bin/bash -e

url=https://foldseek.steineggerlab.workers.dev/pdb100.tar.gz

mkdir -p ../big_dbs/foldseek/pdb100
mkdir -p ../big_dbs/reseek/pdb100
mkdir -p ../big_downloads

cdir=$PWD

if [ ! -s ../big_downloads/pdb100.tar.gz ] ; then
	cd ../big_downloads
	wget $url
fi

cd ../big_dbs/foldseek/pdb100
tar -zxvf $cdir/../big_downloads/pdb100.tar.gz
