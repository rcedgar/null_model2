#!/bin/bash -e

for db in \
	bfvd \
	pdb
do
	./reseek_search.bash scop40 $db
	./foldseek_search.bash scop40 $db
done

for db in \
	cath40 \
	scop95
do
	./reseek_search.bash $db $db
	./foldseek_search.bash $db $db
done

for db in \
	scop40_div2 \
	scop40_div4 \
	scop40 \
	scop40x2 \
	scop40x4 \
	scop40x8
do
	./reseek_search.bash scop40 $db
	./foldseek_search.bash scop40 $db
done
