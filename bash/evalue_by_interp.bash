#!/bin/bash -e

mkdir -p ../evalue_by_interp
cd ../evalue_by_interp

for refdb in scop40 scop40c
do
	if [ $refdb == scop40 ] ; then
		refdbsize=11211
	elif [ $refdb == scop40c ] ; then
		refdbsize=8340
	fi

	python ../py/evalue_by_interp.py \
		--edf ../edf/dali.$refdb \
		--score 40 \
		--steps 20 \
		--delta -2 \
		--refdbsize $refdbsize \
		> dali.$refdb
	
	grep -v "^#" dali.$refdb \
		| ../py/columns.py \
		> dali.$refdb.txt

	if [ $refdb == scop40c ] ; then
		python ../py/evalue_by_interp.py \
			--edf ../edf/tm.$refdb \
			--score 0.75 \
			--steps 6 \
			--delta -0.05 \
			--scorefmt %.2f \
			--refdbsize $refdbsize \
			> tm.$refdb
	else
		python ../py/evalue_by_interp.py \
			--edf ../edf/tm.$refdb \
			--score 0.85 \
			--steps 7 \
			--delta -0.05 \
			--scorefmt %.2f \
			--refdbsize $refdbsize \
			> tm.$refdb
	fi
	
	grep -v "^#" tm.$refdb \
		| ../py/columns.py \
		> tm.$refdb.txt

	if [ $refdb == scop40c ] ; then
		python ../py/evalue_by_interp.py \
			--edf ../edf/foldseek.$refdb \
			--score 8 \
			--steps 8 \
			--delta -1 \
			--evalue \
			--refdbsize $refdbsize \
			> foldseek.$refdb
	else
		python ../py/evalue_by_interp.py \
			--edf ../edf/foldseek.$refdb \
			--score 13 \
			--steps 13 \
			--delta -1 \
			--evalue \
			--refdbsize $refdbsize \
			> foldseek.$refdb
	fi
	
	grep -v "^#" foldseek.$refdb \
		| ../py/columns.py \
		> foldseek.$refdb.txt

	if [ $refdb == scop40c ] ; then
		python ../py/evalue_by_interp.py \
			--edf ../edf/reseek.$refdb \
			--score 10 \
			--steps 13 \
			--delta -1 \
			--evalue \
			--refdbsize $refdbsize \
			> reseek.$refdb
	else
		python ../py/evalue_by_interp.py \
			--edf ../edf/reseek.$refdb \
			--score 10 \
			--steps 13 \
			--delta -1 \
			--evalue \
			--refdbsize $refdbsize \
			> reseek.$refdb
	fi
	
	grep -v "^#" reseek.$refdb \
		| ../py/columns.py \
		> reseek.$refdb.txt
done
