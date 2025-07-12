#!/usr/bin/python3

import sys
import math
import argparse
import numpy as np

AP = argparse.ArgumentParser()
AP.add_argument("--scores", required=True, help="Scores file")
AP.add_argument("--field", type=int, default=1)
AP.add_argument("--minscore", required=True, type=float)
AP.add_argument("--binwidth", required=True, type=float)
AP.add_argument("--bins", required=True, type=int, default=32, help="Nr. bins")
AP.add_argument("--evalues", default=False, action="store_true")
AP.add_argument("--output", required=False, type=str, help="Output TSV")
Args = AP.parse_args()

fldidx = Args.field - 1

nrbins = Args.bins

maxscore = Args.minscore + Args.binwidth*Args.bins
binedges = []
for binidx in range(Args.bins+1):
	binedges.append(Args.minscore + binidx*Args.binwidth)

scores = []
for line in open(Args.scores):
	flds = line[:-1].split('\t')
	score = float(flds[fldidx])
	if Args.evalues:
		if score < 1e-40:
			score = 1e-40
		score = -math.log10(score)
	if score < Args.minscore or score > maxscore:
		continue
	scores.append(score)

scores = np.array(scores, dtype=np.float32)
h, binedges_ = np.histogram(scores, binedges)

if not Args.output is None:
	with open(Args.output, "w") as ftsv:
		for bin_idx in range(nrbins):
			s = "%.5g" % binedges[bin_idx]
			s += "\t%d" % h[bin_idx]
			ftsv.write(s + '\n')
