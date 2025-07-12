#!/bin/bash -e

####################
# WARNING          
####################
rm -f ../edf/tm*
####################

#              	mode  ref		q		db			dbdupes	divn	divsf
#----------------------------------------------------------------------------------------
./edf_tm.bash 	none scop40		scop40	scop40		1		1		1
./edf_tm.bash 	none scop40c	scop40	scop40		1		1		1

./edf_tm.bash 	none scop40		scop40	scop40		1		2		1
./edf_tm.bash 	none scop40		scop40	scop40		1		4		1

./edf_tm.bash 	none scop40		scop40	scop40		1		1		2
./edf_tm.bash 	none scop40		scop40	scop40		1		1		4

./edf_tm.bash 	none scop40		scop40	scop40		1		1		2
./edf_tm.bash 	none scop40		scop40	scop40		1		1		4
