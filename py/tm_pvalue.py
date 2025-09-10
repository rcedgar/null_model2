#!/usr/bin/python3

import sys
import math
import argparse
import numpy as np
from read_dist import read_dist

scores, N_scores = read_dist("../edf/tm.scop40.scop40.scop40", "N_score")

nrbins = len(scores)
N = 0
n = 0
for binidx in range(nrbins):
	score = scores[binidx]
	hits = N_scores[binidx]
	N += hits
	if score >= 0.5:
		n += hits

print("%.3e" % (n/N))