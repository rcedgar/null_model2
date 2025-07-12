#!/bin/bash -e

if [ -s ../big_foldseek_db_scop95/scop95 ] ; then
	echo =====================================
	echo ../big_foldseek_db_scop95/scop95 done
	echo =====================================
	exit 0
fi

mkdir -p ../big_foldseek_db_scop95
cd ../big_foldseek_db_scop95

foldseek-v10 createdb ../big_pdb_scop95/fixed_pdbs scop95
