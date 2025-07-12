#!/usr/bin/python3

import os
import sys
import math

# hit counts:

# make_reseek_afdb100k_subset.bash
#     22145 ../big_hits/reseek_fast_afdb_100ksubset.tsv
#   5203370 ../big_hits/reseek_sensitive.scop40.afdb100k

fastfn = "../big_hits/reseek_fast_afdb_100ksubset.tsv"		# 1=scop40, 2=afdb, 3=newts
fullfn = "../big_hits/reseek_sensitive.scop40.afdb100k"		# 1=scop40, 2=afdb, 3=evalue, 4=dpscore, 5=newts

mints = 0.05
maxts = 1.05

nrbins = 101

def get_binidx(ts):
	binidx = int((ts - mints)/(maxts - mints)*(nrbins-1) + 0.5)
	return binidx

def get_ts(binidx):
	return mints + binidx*(maxts - mints)/(nrbins - 1)

def read_hits(hitsfn, fldidx):
	counts = [0]*nrbins
	for line in open(hitsfn):
		flds = line[:-1].split('\t')
		q = flds[0]
		acc = flds[1]
		newts = float(flds[fldidx])
		binidx = get_binidx(newts)
		if binidx >= 0 and binidx < nrbins:
			counts[binidx] += 1
	return counts

if 0:
	for binidx in range(nrbins):
		ts = get_ts(binidx)
		binidx2 = get_binidx(ts)
		print(binidx, binidx2, "%.3g" % ts)

counts_fast = read_hits(fastfn, 2)
counts_full = read_hits(fullfn, 4)

s = "newts"
s += "\tN_all"
s += "\tN_fast"
s += "\tP"
print(s)
for binidx in range(nrbins):
	newts = get_ts(binidx)
	count_all = counts_full[binidx]
	count_fast = counts_fast[binidx]
	P = 0
	if count_all > 0:
		P = count_fast/count_all

	s = "%.3g" % newts
	s += "\t%d" % count_all
	s += "\t%d" % count_fast
	s += "\t%.3g" % min(P, 1)
	print(s)
