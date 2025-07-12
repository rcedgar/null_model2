#!/bin/bash -e

if [ ! -s ../big_downloads/scop40pdb.tar.gz ] ; then
	echo Downloading
	mkdir -p ../big_downloads
	cd ../big_downloads
	wget https://wwwuser.gwdg.de/~compbiol/foldseek/scop40pdb.tar.gz
fi

if [ ! -s ../big_scop40pdb/d8abpa_.pdb ] ; then
	mkdir -p ../big_scop40pdb
	cd ../big_scop40pdb
	echo Extracting
	tar -zxf ../big_downloads/scop40pdb.tar.gz
	echo Adding .pdb extension
	for x in `ls pdb/`
	do
		mv pdb/$x $x.pdb
	done
	rmdir pdb
fi

dbdir=../big_dbs/reseek
mkdir -p $dbdir

cp -v ../big_data/scop40.bca $dbdir/scop40.bca
cp -v ../big_data/scop95.bca $dbdir/scop95.bca
cp -v ../big_data/cath40.bca $dbdir/cath40.bca

dbdir=../big_dbs/foldseek/scop40
mkdir -p $dbdir

foldseek-v10 \
	createdb \
	../big_scop40pdb \
	$dbdir/scop40

mkdir -p ../big_data

../bin/reseek \
	-convert ../big_scop40pdb \
	-nochainchar \
	-bca ../big_data/scop40.bca \
	-cal ../big_data/scop40.cal

../bin/reseek \
	-convert_foldseekdb $dbdir/scop40 \
	-cal ../big_data/scop40.fs.cal \
	-3di ../big_data/scop40.3di.fa \
	-log ../tmp/convert.log

../bin/reseek \
	-convert ../big_data/scop40.fs.cal \
	-bca ../big_data/scop40.fs.bca
