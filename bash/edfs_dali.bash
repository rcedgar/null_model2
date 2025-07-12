#!/bin/bash -e

####################
# WARNING          
####################
rm -f ../edf/dali*
####################

#                 	mode  ref				q		db			dbdupes	divn	divsf
#----------------------------------------------------------------------------------------
./edf_dali.bash 	none scop40				scop40	scop40		1		1		1
./edf_dali.bash 	none scop40c			scop40	scop40		1		1		1

./edf_dali.bash 	none scop40				scop40	scop40		1		2		1
./edf_dali.bash 	none scop40				scop40	scop40		1		4		1

./edf_dali.bash 	none scop40				scop40	scop40		1		1		2
./edf_dali.bash 	none scop40				scop40	scop40		1		1		4

./edf_dali.bash 	none scop40				scop40	scop40		1		1		2
./edf_dali.bash 	none scop40				scop40	scop40		1		1		4
