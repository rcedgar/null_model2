#!/bin/bash -e

cd ../big_hits

name=backup_big_data_hits_2025-06-10

tar --hard-dereference -h -zcvf ../tmp/$name.tz \
	tm.scop40 \
	dali.scop40 \
	reseek_fast.scop40.afdb50 \
	foldseek_default.scop40.afdb50

aws s3 cp ../tmp/$name.tz s3://serratus-reseek/big_hits/

aws s3 cp ../bash/$0 s3://serratus-reseek/big_hits/bash
