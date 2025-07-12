#!/bin/bash -e

mkdir -p ../big_pdb_scop95
cd ../big_pdb_scop95

wget \
	--no-check-certificate \
	https://scop.berkeley.edu/downloads/pdbstyle/pdbstyle-sel-gs-bib-95-2.08.tgz

tar -zxf pdbstyle-sel-gs-bib-95-2.08.tgz
rm -f pdbstyle-sel-gs-bib-95-2.08.tgz

cd  pdbstyle-2.08
find | grep "\.ent$" > ../ent.files
