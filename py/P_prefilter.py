#!/usr/bin/python3

# P_prefilter2 uses P_prefilter/algo*subsets.tsv for P(pass_prefilter|s)

import sys
import math
import argparse
import numpy as np
from read_dist import read_dist

AP = argparse.ArgumentParser()
AP.add_argument("--edf", required=True)			# for P_score_F
AP.add_argument("--hist_all", required=True)
AP.add_argument("--hist_pre", required=True)
Args = AP.parse_args()

scores, P_score_Fs = read_dist(Args.edf, "P_score_F")

def read_hist(fn):
	bin_mids = []
	v = []
	for line in open(fn):
		if line.startswith('#'):
			continue
		if len(line.strip()) == 0:
			continue
		flds = line[:-1].split('\t')
		bin_mid = float(flds[0])
		x = float(flds[1])
		bin_mids.append(bin_mid)
		v.append(x)
	return bin_mids, v

bin_mids_all, N_all = read_hist(Args.hist_all)
bin_mids_pre, N_pre = read_hist(Args.hist_pre)
assert bin_mids_all == bin_mids_pre

scores2 = []
P_pres = []

for binidx in range(len(bin_mids_all)):
	score = bin_mids_all[binidx]
	n_all = N_all[binidx]
	n_pre = N_pre[binidx]
	P_pass_prefilter = 0
	if n_all > 0:
		P_pass_prefilter = n_pre/n_all
	scores2.append(score)
	P_pres.append(P_pass_prefilter)

s = "score"
s += "\tP_score_F"
s += "\tP_pre"
s += "\tPP"
print(s)
for binidx in range(len(scores)):
	score = scores[binidx]
	P_score_F = P_score_Fs[binidx]
	P_pre = np.interp(score, scores2, P_pres)
	s = "%.3g" % score
	s += "\t%.3g" % P_score_F
	s += "\t%.3g" % P_pre
	s += "\t%.3g" % (P_score_F*P_pre)
	print(s)
