#!/usr/bin/python3

import os
import sys
import math

algo = sys.argv[1]

if algo == "reseek":
	fastfn = "../big_data/hits/reseek_fast.scop40.afdb50"
elif algo == "foldseek":
	fastfn = "../big_data/hits/foldseek_default.scop40.afdb50"
else:
	assert False

accs = set()
acc2allhits = {}
for subsetidx in range(10):
	subset = "%03d" % (subsetidx+1)
	accsfn = "../big_data/hits/scop40_vs_random10kAFDB/" + subset + ".accs"
	for acc in open(accsfn):
		acc = acc[:-1]
		accs.add(acc)
		acc2allhits[acc] = set()

nrbins = 22
counts_fast = [0]*nrbins
counts_all = [0]*nrbins

for subsetidx in range(10):
	subset = "%03d" % (subsetidx+1)
	if algo == "reseek":
		hitsfn = "../big_data/hits/scop40_vs_random10kAFDB/" \
			"reseek_sensitive_scop40_vs_random10k_afdb50_" + subset + ".tsv"
	else:
		hitsfn = "../big_data/hits/scop40_vs_random10kAFDB/" \
			"foldseek_exhaustive_scop40_vs_random10k_afdb50_" + subset + ".tsv"
	sys.stderr.write(hitsfn + '\n')
	for line in open(hitsfn):
		flds = line[:-1].split('\t')
		q = flds[0]
		acc = flds[1]
		assert acc in accs
		acc2allhits[acc].add(q)
		evalue = float(flds[2])
		if evalue < 1e-20:
			continue
		score = -math.log10(evalue)
		binidx = round(score) + 1
		if binidx < 0 or binidx >= nrbins:
			continue
		counts_all[binidx] += 1

n = 0
total = 0
found = 0
sys.stderr.write(fastfn + '\n')
filesize = os.path.getsize(fastfn)
for line in open(fastfn):
	n += 1
	total += len(line) + 1
	if n%10000 == 0:
		pct = total*100/filesize
		sys.stderr.write("%.3g%%     \r" % (pct))
	flds = line[:-1].split('\t')
	if algo == "foldseek":
		q = flds[0]
		acc = flds[1]
	else:
		q = flds[1]
		acc = flds[0][:-1] # remove spurious chain 'A' from acc
	if not acc in accs:
		continue
	found += 1
	if algo == "foldseek":
		evalue = float(flds[3])
	else:
		evalue = float(flds[2])
	if evalue < 1e-20:
		continue
	score = -math.log10(evalue)
	binidx = round(score) + 1
	if binidx < 0 or binidx >= nrbins:
		continue
	counts_fast[binidx] += 1
sys.stderr.write("100.0%        \n")

s = "score"
s += "\tE-value"
s += "\tN_all"
s += "\tN_fast"
s += "\tP"
print(s)
for binidx in range(nrbins):
	score = binidx - 1
	evalue = 10**(-score)
	count_all = counts_all[binidx]
	count_fast = counts_fast[binidx]
	P = 0
	if count_all > 0:
		P = count_fast/count_all

	s = "%d" % score
	s += "\t%.3g" % evalue
	s += "\t%d" % count_all
	s += "\t%d" % count_fast
	s += "\t%.3g" % P
	print(s)
