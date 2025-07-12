#!/bin/bash -e

####################
# WARNING          
####################
rm -f ../edf/reseek*
####################

#                 		mode  ref			q		db				dbdupes	divn	divsf
#--------------------------------------------------------------------------------------------
mode=rsbsize100
./edf_reseek.bash 		$mode scop40_div4	scop40	scop40_div4		1		1		1
./edf_reseek.bash 		$mode scop40_div2	scop40	scop40_div2		1		1		1
./edf_reseek.bash 		$mode scop40		scop40	scop40			1		1		1
./edf_reseek.bash 		$mode scop40		scop40	scop40x2		2		1		1
./edf_reseek.bash 		$mode scop40		scop40	scop40x4		4		1		1
./edf_reseek.bash 		$mode scop40		scop40	scop40x8		8		1		1

mode=verysensitive
./edf_reseek.bash 		$mode scop40		scop40	scop40			1		1		1

mode=fast
./edf_reseek.bash 		$mode none			scop40	afdb50		1		1		1
# cannot do sensitive, reseek_sensitive.scop40.afdb50 is 68Gb

for mode in fast sensitive
do
	#                 	mode ref				q		db			dbdupes	divn	divsf
	#----------------------------------------------------------------------------------------

	./edf_reseek.bash 	$mode none				scop40	bfvd		1		1		1
	./edf_reseek.bash 	$mode none				scop40	pdb			1		1		1
	./edf_reseek.bash 	$mode scop95			scop95	scop95		1		1		1
	./edf_reseek.bash 	$mode cath40			cath40	cath40		1		1		1

	./edf_reseek.bash 	$mode scop40_div2		scop40	scop40_div2	1		1		1
	./edf_reseek.bash 	$mode scop40_div4		scop40	scop40_div4	1		1		1

	./edf_reseek.bash 	$mode scop95_cluster70	scop95	scop95		1		1		1
	./edf_reseek.bash 	$mode scop95_cluster40	scop95	scop95		1		1		1

	./edf_reseek.bash 	$mode scop40			scop40	scop40		1		1		1
	./edf_reseek.bash 	$mode scop40c			scop40	scop40		1		1		1

	./edf_reseek.bash 	$mode scop40			scop40	scop40		1		2		1
	./edf_reseek.bash 	$mode scop40			scop40	scop40		1		4		1

	./edf_reseek.bash 	$mode scop40			scop40	scop40		1		1		2
	./edf_reseek.bash 	$mode scop40			scop40	scop40		1		1		4

	./edf_reseek.bash 	$mode scop40			scop40	scop40x2	2		1		1
	./edf_reseek.bash 	$mode scop40			scop40	scop40x4	4		1		1
	./edf_reseek.bash 	$mode scop40			scop40	scop40x8	8		1		1
done
