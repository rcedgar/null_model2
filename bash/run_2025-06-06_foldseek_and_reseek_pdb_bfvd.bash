#!/bin/bash -e

for db in \
	bfvd \
	pdb
do
	./reseek_search.bash scop40 $db
	./foldseek_search.bash scop40 $db
done
