#!/bin/bash -e

if [ ! -d ../big_cath40pdb ] ; then
	if [ ! -s ../tmp_download/cath-dataset-nonredundant-S40.pdb.tgz ] ; then
		mkdir -p ../tmp_download
		cd ../tmp_download
		wget http://download.cathdb.info/cath/releases/latest-release/non-redundant-data-sets/cath-dataset-nonredundant-S40.pdb.tgz
	fi

	echo Extracting
	cd ..
	tar -zxf tmp_download/cath-dataset-nonredundant-S40.pdb.tgz
	mv dompdb big_cath40pdb
	cd big_cath40pdb

	echo Adding .pdb extension
	for x in *
	do
		mv $x $x.pdb
	done
fi

dbdir=../big_dbs/foldseek/cath40
mkdir -p $dbdir

foldseek-v10 \
	createdb \
	../big_cath40pdb \
	$dbdir/cath40

mkdir -p ../big_data

../bin/reseek \
	-convert ../big_cath40pdb \
	-nochainchar \
	-bca ../big_data/cath40.bca \
	-cal ../big_data/cath40.cal

../bin/reseek \
	-convert_foldseekdb $dbdir/cath40 \
	-bca ../big_data/cath40.fs.bca \
	-cal ../big_data/cath40.fs.cal \
	-3di ../big_data/cath40.3di.fa
