#!/usr/bin/python3

# Make EDF file from E-values field, 
# calculates N(score), M(score) and P(score) only

import sys
import math
import argparse
import numpy as np
import dbname2size
import foldseek_evalue_calc

AP = argparse.ArgumentParser()
AP.add_argument("--hits", required=True)
AP.add_argument("--field", required=True, type=int)
AP.add_argument("--qname", required=False, type=str, default="scop40")
AP.add_argument("--dbname", required=False, type=str, default="scop40")
AP.add_argument("--bins", type=int, default=100)
AP.add_argument("--evalues", default=False, action="store_true")
AP.add_argument("--minevalue", type=float, default=1e-20)
AP.add_argument("--maxevalue", type=float, default=1000)
AP.add_argument("--minscore", type=float)
AP.add_argument("--maxscore", type=float)
AP.add_argument("--foldseek", choices = [ "evalue", "score"], default=None)
Args = AP.parse_args()

if not Args.foldseek is None:
	assert Args.evalues
	assert not Args.dbname is None
	searchdbname = Args.dbname

if Args.evalues:
	minscore = -math.log10(Args.maxevalue)
	maxscore = -math.log10(Args.minevalue)
else:
	assert not Args.minscore is None
	assert not Args.maxscore is None
	minscore = Args.minscore
	maxscore = Args.maxscore

qname, dbname = dbname2size.get_names(Args.hits, None)

nrbins = Args.bins
fi = Args.field - 1

nrhits = 0
scores = []
for line in open(Args.hits):
	if line.startswith("query"):
		continue
	flds = line[:-1].split('\t')
	x = float(flds[fi])
	if Args.foldseek == "score":
		x = foldseek_evalue_calc. \
			convert_evalue3(x, searchdbname, "afdb50")
	if Args.evalues:
		E = x
		if E > Args.maxevalue:
			continue
		if E < Args.minevalue:
			E = Args.minevalue
		score = -math.log10(E)
	else:
		score = x
		if score < minscore:
			continue
		if score > maxscore:
			score = maxscore
	scores.append(score)
	nrhits += 1

binmids = np.linspace(minscore, maxscore, nrbins)
binedges = np.linspace(minscore, maxscore, nrbins+1)

n = len(scores)
total = sum(scores)
N_score, _ = np.histogram(scores, binedges)
M_score = np.cumsum(N_score[::-1])[::-1]

print("binmids\tN_score\tM_score")

# total hits included in calculation
H = 0
for binidx in range(nrbins):
	score = binmids[binidx]
	N = N_score[binidx]
	H += N
	P = N/total
	s = "%.4g" % score
	s += "\t%d" % N
	s += "\t%d" % M_score[binidx]
	s += "\t%d" % P
	print(s)

dbsize = dbname2size.dbname2size[dbname]
qsize = dbname2size.dbname2size[qname]

s = "# "
s += "q=%s;" % Args.qname
s += "qsize=%d;" % qsize
s += "db=%s;" % Args.dbname
s += "dbsize=%d;" % dbsize
s += "ref=none;"
s += "hits=%d;" % nrhits
s += "hitrate=%.3g;" % (nrhits/(dbsize*qsize))
print(s)

print('# ' + ' '.join(sys.argv))

sys.stderr.write(s + '\n')
