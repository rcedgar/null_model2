#!/bin/bash -e

./download_scop.bash

mkdir -p ../big_dbs/reseek
mkdir -p ../big_scop95pdb
cd ../big_scop95pdb

if [ ! -d pdbstyle-2.08 ] ; then
	if [ ! -s pdbstyle-sel-gs-bib-95-2.08.tgz ] ; then
		wget \
			--no-check-certificate \
			https://scop.berkeley.edu/downloads/pdbstyle/pdbstyle-sel-gs-bib-95-2.08.tgz
	fi
	tar -zxf pdbstyle-sel-gs-bib-95-2.08.tgz
fi

find pdbstyle-2.08 \
	| grep "\.ent$" \
	> ent.files

cut -d/ -f3 ent.files \
	| sed "-es/\.ent//" \
	> scop95_withb1.doms

fgrep -Ff scop95_withb1.doms \
	../big_scop_2.08/dir.des.scope.2.08-stable.txt \
	| sed "-es/  */\t/" \
	| cut -f3,4  \
	| sed "-es/\(.*\)\t\(.*\)/\2\t\1/" \
	> scop95_withb1.lookup

# Remove anomalous superfamily b.1.1 (Ig, antibodies)
fgrep -v b.1.1. scop95_withb1.lookup \
	> scop95.lookup

cut -f1 scop95.lookup \
	> scop95.doms

# First model only
python ../py/pdbs_scop95_extract_first_model.py

reseek \
	-convert fixed_pdbs/ \
	-nochainchar \
	-cal scop95_noscopid.cal

python ../py/add_scopid_to_cal.py \
	scop95_noscopid.cal \
	scop95.lookup \
	> ../big_dbs/reseek/scop95.cal

reseek \
	-convert ../big_dbs/reseek/scop95.cal \
	-bca ../big_dbs/reseek/scop95.bca

currdir=$PWD

mkdir -p ../big_dbs/foldseek/scop95
cd ../big_dbs/foldseek/scop95

foldseek-v10 createdb $currdir/fixed_pdbs scop95
