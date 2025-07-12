#!/usr/bin/python3

import os
import sys
import math

algo = sys.argv[1]

# hit counts:

#     22145 ../tmp/reseek_fast_afdb_100ksubset.tsv
#   5203370 ../big_hits/reseek_sensitive.scop40.afdb100k

#     12964 ../tmp/foldseek_default_afdb_100ksubset.tsv
#  22311562 ../big_hits/foldseek_exhaustive.scop40.afdb100k
 
if algo == "reseek":
	fastfn = "../tmp/reseek_fast_afdb_100ksubset.tsv"			# 1=scop40, 2=afdb, 3=evalue
	fullfn = "../big_hits/reseek_sensitive.scop40.afdb100k"		# 1=scop40, 2=afdb, 3=evalue, 3=dpscore, 4=newts
elif algo == "foldseek":
	fastfn = "../tmp/foldseek_default_afdb_100ksubset.tsv"		# 1=scop40, 2=afdb, 3=evalue
	fullfn = "../big_hits/foldseek_exhaustive.scop40.afdb100k"	# 1=scop40, 2=afdb, 3=evalue, 4=bits, 5=prob
else:
	assert False

nrbins = 22

pairs = set()
def read_hits(hitsfn):
	pair2evalue = {}
	for line in open(hitsfn):
		flds = line[:-1].split('\t')
		q = flds[0]
		acc = flds[1]
		evalue = flds[2]
		if float(evalue) > 10:
			continue
		pair = (q, acc)
		pairs.add(pair)
		pair2evalue[pair] = evalue
	return pair2evalue

pair2evalue_fast = read_hits(fastfn)
pair2evalue_full = read_hits(fullfn)

for pair in pairs:
	evalue_fast = pair2evalue_fast.get(pair, ".")
	evalue_full = pair2evalue_full.get(pair, ".")
	if evalue_fast != "." and evalue_full != ".":
		msg = "both"
	elif evalue_fast == ".":
		msg = "nofast"
	elif evalue_full == ".":
		msg = "nofull"
	else:
		assert False
	s = pair[0]
	s += "\t" + pair[1]
	s += "\t" + evalue_full
	s += "\t" + evalue_fast
	s += "\t" + msg
	print(s)

