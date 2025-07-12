#!/bin/bash -e

cd ../edf

(
for mode in fast sensitive
do
	for x in \
		reseek_${mode}_ts.scop40.scop40.scop40 \
		reseek_${mode}_ts.scop40.bfvd.none \
		reseek_${mode}_ts.scop40.pdb.none
	do
		grep -H hitrate= $x \
			| sed "-es/:.*hitrate=/\t/" \
			| sed "-es/;.*//"
	done
done

for x in \
	reseek_fast_ts.scop40.afdb50.none
do
	grep -H hitrate= $x \
		| sed "-es/:.*hitrate=/\t/" \
		| sed "-es/;.*//"
done
) \
	| sed "-es/reseek_//" \
	| sed "-es/_ts//" \
	| sed "-es/\./\t/" \
	| sed "-es/\./\t/" \
	| sed "-es/\./\t/" \
	| cut -f1,3,5
