#!/usr/bin/python3

# P_prefilter2 uses P_prefilter/algo*subsets.tsv for P(pass_prefilter|s)
# subsets.tsv generated by P_pass_prefilter.py

import sys
import math
import argparse
import numpy as np
from read_dist import read_dist

AP = argparse.ArgumentParser()
AP.add_argument("--edf", required=True)			# for P_score_F
AP.add_argument("--passtsv", required=True)		# output from P_pass_prefilter.py
Args = AP.parse_args()

scores, P_score_Fs = read_dist(Args.edf, "P_score_F")

scores2 = []
P_passv = []
f = open(Args.passtsv)
hdr = f.readline()
assert hdr.startswith("score\tE-value")
for line in f:
	flds = line[:-1].split('\t')
	assert len(flds) == 5
	score = float(flds[0])
	P = float(flds[4])
	scores2.append(score)
	P_passv.append(P)

s = "score"
s += "\tP_score_F"
s += "\tP_pre"
s += "\tPP"
print(s)
for binidx in range(len(scores)):
	score = scores[binidx]
	P_score_F = P_score_Fs[binidx]
	P_pass = np.interp(score, scores2, P_passv)
	s = "%.3g" % score
	s += "\t%.3g" % P_score_F
	s += "\t%.3g" % P_pass
	s += "\t%.3g" % (P_score_F*P_pass)
	print(s)
