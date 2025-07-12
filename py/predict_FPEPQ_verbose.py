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
AP.add_argument('--edf_ref', required=False, type=str, default="../edf/reseek.scop40")
AP.add_argument('--edf_target', required=False, type=str, default="../edf/reseek.scop40")
AP.add_argument('--target_query_size', required=False, type=float, default=11211)
AP.add_argument('--ref_query_size', required=False, type=float, default=11211)
AP.add_argument('--output', type=str, required=False, default="/dev/stdout")
AP.add_argument('--evalues', default=False, action="store_true")
AP.add_argument('--plot', type=str, required=False, help="Plot file, default none")
AP.add_argument('--xrange', type=str, required=False, help="xlo,xhi")
AP.add_argument('--yrange', type=str, required=False, default="1e-3:100", help="ylo,yhi")
Args = AP.parse_args()

NQ_ref = Args.ref_query_size
NQ_target = Args.target_query_size

xlim = None
if not Args.xrange is None:
	flds = Args.xrange.replace('_', '-').split(':')
	assert len(flds) == 2
	xlim = [ float(flds[0]), float(flds[1]) ]

ylim = None
if not Args.yrange is None:
	flds = Args.yrange.replace('_', '-').split(':')
	assert len(flds) == 2
	ylim = [ float(flds[0]), float(flds[1]) ]

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
		assert len(scores_) == len(scores)
		assert scores_[0] == scores[0]
		assert scores_[-1] == scores[-1]
	dist_dict[name] = dist
	return dist

N_score_Ts_ref = read_dist_dict(Args.edf_ref, "N_score_T")
N_score_Ts_target = read_dist_dict(Args.edf_target, "N_score_T")

N_score_Fs_ref = read_dist_dict(Args.edf_ref, "N_score_F")
N_score_Fs_target = read_dist_dict(Args.edf_target, "N_score_F")

N_scores_ref = read_dist_dict(Args.edf_ref, "N_score")
N_scores_target = read_dist_dict(Args.edf_target, "N_score")

FPEPQs_ref = read_dist_dict(Args.edf_ref, "cve_epq")
FPEPQs_target = read_dist_dict(Args.edf_target, "cve_epq")

fout = open(Args.output, "w")

NHT_ref = sum(N_score_Ts_ref)
NHT_target = sum(N_score_Ts_target)

NHF_ref = sum(N_score_Fs_ref)
NHF_target = sum(N_score_Fs_target)

NH_ref = NHT_ref + NHF_ref
NH_target = NHT_target + NHF_target

NH_ref = sum(N_scores_ref)
NH_target = sum(N_scores_target)

PF_ref = NHF_ref/NH_ref
PF_target = NHF_target/NH_target
fout.write("# PF_ref=%.3g, PF_target=%.3g\n" % (PF_ref, PF_target))

N_scores_ref = []
N_scores_target = []

N_scores_T_ref = []
N_scores_T_target = []

N_scores_F_ref = []
N_scores_F_target = []

P_scores_ref = []
P_scores_target = []

P_scores_F_ref = []
P_scores_F_target = []

P_F_scores_ref = []
P_F_scores_target = []

for binidx in range(nrbins):
	score = scores[binidx]

	N_score_T_ref = N_score_Ts_ref[binidx]
	N_score_T_target = N_score_Ts_target[binidx]

	N_score_F_ref = N_score_Fs_ref[binidx]
	N_score_F_target = N_score_Fs_target[binidx]

	N_score_ref = N_score_T_ref + N_score_F_ref
	N_score_target = N_score_T_target + N_score_F_target

	assert N_score_F_ref <= N_score_ref
	assert N_score_F_target <= N_score_target

	P_score_ref = N_score_ref/NH_ref
	P_score_target = N_score_target/NH_target

	P_score_F_ref = N_score_F_ref/NHF_ref
	P_score_F_target = N_score_F_target/NHF_target

	P_F_score_ref = 0
	if N_score_ref > 0:
		P_F_score_ref = N_score_F_ref/N_score_ref

	P_F_score_target = 0
	if N_score_target > 0:
		P_F_score_target = N_score_F_target/N_score_target

	if P_score_ref > 0:
		P_F_score_Bayes_ref = PF_ref*P_score_F_ref/P_score_ref
		if abs(P_F_score_Bayes_ref - P_F_score_ref) > 0.1:
			sys.stderr.write(f"WARNING {score=:.3g} {P_F_score_Bayes_ref=:.3g} {P_F_score_ref=:.3g}\n")
			sys.stderr.write(f"  {P_score_F_ref=:.3g} {P_score_ref=:.3g}\n")
			# assert False

	if P_score_target > 0:
		P_F_score_Bayes_target = PF_target*P_score_F_target/P_score_target
		# print(f"{P_score_F_target=}")
		# print(f"{P_score_target=}")
		if abs(P_F_score_Bayes_target - P_F_score_target) > 0.1:
			sys.stderr.write(f"WARNING {score=:.3g} {P_F_score_Bayes_target=:.3g} {P_F_score_target=:.3g}\n")
			# assert False

	N_scores_ref.append(N_score_ref)
	N_scores_target.append(N_score_target)

	N_scores_T_ref.append(N_score_T_ref)
	N_scores_T_target.append(N_score_T_target)

	N_scores_F_ref.append(N_score_F_ref)
	N_scores_F_target.append(N_score_F_target)

	P_scores_ref.append(P_score_ref)
	P_scores_target.append(P_score_target)

	P_scores_F_ref.append(P_score_F_ref)
	P_scores_F_target.append(P_score_F_target)

	P_F_scores_ref.append(P_F_score_ref)
	P_F_scores_target.append(P_F_score_target)

def estimate_FPEPQ_ref_self(binidxz):
	FPEPQ = 0
	for binidx2 in range(binidx, nrbins):
		FPEPQ += PF_ref*(NH_ref/NQ_ref)*P_scores_F_ref[binidx2]
	return FPEPQ

def estimate_FPEPQ_target_self(binidxz):
	FPEPQ = 0
	for binidx2 in range(binidx, nrbins):
		FPEPQ += PF_target*(NH_target/NQ_target)*P_scores_F_target[binidx2]
	return FPEPQ

def estimate_FPEPQ_target(binidxz):
	FPEPQ = 0
	for binidx2 in range(binidx, nrbins):
		FPEPQ += PF_target*(NH_target/NQ_target)*P_scores_F_ref[binidx2]
	return FPEPQ

FPEPQs_ref_est = []
FPEPQs_target_est = []
FPEPQs_target_pred = []

for binidx in range(nrbins):
	FPEPQs_ref_est.append(estimate_FPEPQ_ref_self(binidx))
	FPEPQs_target_est.append(estimate_FPEPQ_target_self(binidx))
	FPEPQs_target_pred.append(estimate_FPEPQ_target(binidx))

s = "score"
if Args.evalues:
	s += "\tE-value"
s += "\tP_score_F_ref"
s += "\tP_score_F_target"
s += "\tFPEPQ_ref"
s += "\tFPEPQ_ref_est"
s += "\tFPEPQ_target"
s += "\tFPEPQ_target_self"
s += "\tFPEPQ_target_pred"
if not fout is None:
	fout.write(s + '\n')

for binidx in range(nrbins):
	score = scores[binidx]

	FPEPQ_ref = FPEPQs_ref[binidx]
	FPEPQ_ref_est = FPEPQs_ref_est[binidx]
	FPEPQ_target = FPEPQs_target[binidx]
	FPEPQ_target_est = FPEPQs_target_est[binidx]
	FPEPQ_target_pred = FPEPQs_target_pred[binidx]

	s = "%.3g" % score
	if Args.evalues:
		s += "\t%.3g" % 10**(-score)
	s += "\t%.3g" % P_scores_F_ref[binidx]
	s += "\t%.3g" % P_scores_F_target[binidx]
	s += "\t%.3g" % FPEPQ_ref
	s += "\t%.3g" % FPEPQ_ref_est
	s += "\t%.3g" % FPEPQ_target
	s += "\t%.3g" % FPEPQ_target_est
	s += "\t%.3g" % FPEPQ_target_pred
	if not fout is None:
		fout.write(s + '\n')

	if FPEPQ_target < 1e-4 and FPEPQ_target_pred < 1e-4:
		break

fig, ax = plt.subplots(1, 1)
ax.set_title("Bayes predict FPEPQ\nref=%s\ntarget=%s" \
	% (Args.edf_ref, Args.edf_target))
ax.set_xlabel("score")
ax.set_ylabel("FPEPQ")
ax.set_yscale('log')
if not xlim is None:
	ax.set_xlim(xlim)
if not ylim is None:
	ax.set_ylim(ylim)

ax.plot(scores, FPEPQs_target, label = "Measured", color="blue", linestyle="dashdot")
ax.plot(scores, FPEPQs_target_pred, label = "Predicted", color="magenta", linestyle="dotted")
ax.plot(scores, FPEPQs_ref, label = "Ref", color = "lightgray")
ax.figure.set_size_inches(4.5, 3)
fig.tight_layout()
ax.legend()

if not Args.plot is None:
	sys.stderr.write(Args.plot + '\n')
	fig.savefig(Args.plot)
