#!/usr/bin/python3

import sys
import math
from read_dist import read_dist

edf_sensitive = "../edf/reseek_sensitive_ts.scop40.scop40.scop40"
edf_verysensitive = "../edf/reseek_verysensitive_ts.scop40.scop40.scop40"

scores, counts_sensitive = read_dist(edf_sensitive, "N_score")
scores2, counts_verysensitive = read_dist(edf_verysensitive, "N_score")

nrbins = len(scores)

s = "score"
s += "\tN_verysensitive"
s += "\tN_sensitive"
s += "\tP"
print(s)
for binidx in range(nrbins):
	score = scores[binidx]
	assert scores2[binidx] == score

	count_verysensitive = counts_verysensitive[binidx]
	count_sensitive = counts_sensitive[binidx]
	P = 0
	if count_verysensitive > 0:
		P = count_sensitive/count_verysensitive

	s = "%.3g" % score
	s += "\t%d" % count_verysensitive
	s += "\t%d" % count_sensitive
	s += "\t%.3g" % min(P, 1)
	print(s)
