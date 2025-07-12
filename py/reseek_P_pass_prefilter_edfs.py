#!/usr/bin/python3

import sys
import math
from read_dist import read_dist

searchdb = sys.argv[1]
refdb = sys.argv[2]

mode = "fast"
if len(sys.argv) > 3:
	mode = sys.argv[3]

edf_fast = "../edf/reseek_" + mode + "_ts.scop40." + searchdb + "." + refdb
edf_sensitive = "../edf/reseek_sensitive_ts.scop40." + searchdb + "." + refdb

scores, counts_fast = read_dist(edf_fast, "N_score")
scores2, counts_sensitive = read_dist(edf_sensitive, "N_score")

nrbins = len(scores)

s = "score"
s += "\tN_sensitive"
s += "\tN_fast"
s += "\tP"
print(s)
for binidx in range(nrbins):
	score = scores[binidx]
	assert scores2[binidx] == score

	count_sensitive = counts_sensitive[binidx]
	count_fast = counts_fast[binidx]
	P = 0
	if count_sensitive > 0:
		P = count_fast/count_sensitive

	s = "%.3g" % score
	s += "\t%d" % count_sensitive
	s += "\t%d" % count_fast
	s += "\t%.3g" % min(P, 1)
	print(s)
