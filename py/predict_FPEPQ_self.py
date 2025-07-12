#!/usr/bin/python3

import sys
import argparse
import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from plot_dists_lib import read_dist
from smooth import smooth

matplotlib.use('Agg')

AP = argparse.ArgumentParser()
AP.add_argument('--edf', required=False, type=str, default="../edf/reseek.scop40")
AP.add_argument('--query_size', required=False, type=float, default=11211)
AP.add_argument('--output', type=str, required=False, default="/dev/stdout")
Args = AP.parse_args()

NQ = Args.query_size

scores = None
nrbins = None
dist_dict = {}

def read_dist_dict(fn, name):
	global scores, nrbins
	scores_, dist = read_dist(fn, name)
	if scores is None:
		scores = scores_
		nrbins = len(scores)
	else:
		assert scores_ == scores
	dist_dict[name] = dist
	return dist

N_score_Ts = read_dist_dict(Args.edf, "N_score_T")
N_score_Fs = read_dist_dict(Args.edf, "N_score_F")
FPEPQs = read_dist_dict(Args.edf, "cve_epq")

def get_value(name, binidx):
	dist = dist_dict[name]
	return dist[binidx]

fout = open(Args.output, "w")

NHT = sum(N_score_Ts)
NHF = sum(N_score_Fs)
NH = NHT + NHF
PF = NHF/NH
sys.stderr.write("PF=%.3g\n" % PF)

scoresz = []
N_scoresz = []
N_scores_Tz = []
N_scores_Fz = []
P_scoresz = []
P_scores_Fz = []
P_F_scoresz = []
P_F_scores_Bayesz = []
FPEPQsz = []
for binidx in range(nrbins):
	score = scores[binidx]
	N_score_T = N_score_Ts[binidx]
	N_score_F = N_score_Fs[binidx]
	N_score = N_score_T + N_score_F
	if N_score == 0:
		continue

	P_score = N_score/NH
	P_score_F = N_score_F/NHF

	P_F_score = N_score_F/(N_score_T + N_score_F)

	scoresz.append(score)
	N_scores_Tz.append(N_score_T)
	N_scores_Fz.append(N_score_F)
	N_scoresz.append(N_score)
	P_scoresz.append(P_score)
	P_scores_Fz.append(P_score_F)
	P_F_scoresz.append(P_F_score)

	P_F_score_Bayes = PF*P_score_F/P_score
	if abs(P_F_score_Bayes - P_F_score) > 0.1:
		sys.stderr.write(f"{P_F_score_Bayes=:.3g} {P_F_score=:.3g}\n")
		assert False
	P_F_scores_Bayesz.append(P_F_score_Bayes)

	FPEPQ = get_value("cve_epq", binidx)
	FPEPQsz.append(FPEPQ)

nrbinsz = len(scoresz)

def estimate_FPEPQ(binidxz):
	FPEPQ = 0
	for binidx2 in range(binidxz, nrbinsz):
		FPEPQ += PF*(NH/NQ)*P_scores_Fz[binidx2]
	return FPEPQ

s = "score"
s += "\tN_score"
s += "\tN_score_T"
s += "\tN_score_F"
s += "\tP_score"
s += "\tP_score_F"
s += "\tP_F_score"
s += "\tP_F_score_Bayes"
s += "\tFPEPQ"
s += "\tFPEPQ_pred"
fout.write(s + '\n')

for binidxz in range(nrbinsz):
	FPEPQ_pred = estimate_FPEPQ(binidxz)

	s = "%.3g" % scores[binidxz]
	s += "\t%d" % N_scoresz[binidxz]
	s += "\t%d" % N_scores_Tz[binidxz]
	s += "\t%d" % N_scores_Fz[binidxz]
	s += "\t%.3g" % P_scoresz[binidxz]
	s += "\t%.3g" % P_scores_Fz[binidxz]
	s += "\t%.3g" % P_F_scoresz[binidxz]
	s += "\t%.3g" % P_F_scores_Bayesz[binidxz]
	s += "\t%.3g" % FPEPQsz[binidxz]
	s += "\t%.3g" % FPEPQ_pred
	fout.write(s + '\n')
	if FPEPQsz[binidxz] < 1e-4 and FPEPQ_pred < 1e-4:
		break
fout.close()