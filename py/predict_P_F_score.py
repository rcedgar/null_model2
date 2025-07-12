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
AP.add_argument('--edf_ref', required=True, help="EDF reference tsv")
AP.add_argument('--edf_target', required=True, help="EDF reference tsv")
AP.add_argument('--output', type=str, required=False, help="Output tsv file, default none")
AP.add_argument('--plot', type=str, required=False, help="Plot file, default none")
AP.add_argument('--xrange', type=str, required=False, help="xlo,xhi")
AP.add_argument('--yrange', type=str, required=False, help="ylo,yhi")
AP.add_argument('--prior_pf', type=float, default=0.5)
Args = AP.parse_args()

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

bin_mids, P_F_score_targets = read_dist(Args.edf_target, "P_F_score")
bin_mids2, P_score_F_refs = read_dist(Args.edf_ref, "P_score_F")
bin_mids2a, P_F_score_refs = read_dist(Args.edf_ref, "P_F_score")
bin_mids3, P_score_F_targets = read_dist(Args.edf_target, "P_score_F")
bin_mids4, P_score_targets = read_dist(Args.edf_target, "P_score")

nrbins = len(bin_mids)
for i in range(nrbins):
	assert math.isclose(bin_mids[i], bin_mids2[i], rel_tol=0.001)
	assert math.isclose(bin_mids[i], bin_mids3[i], rel_tol=0.001)
	assert math.isclose(bin_mids[i], bin_mids4[i], rel_tol=0.001)

P_score_targets_smooth = smooth(P_score_targets, 7)

fout = None
if not Args.output is None:
	fout = open(Args.output, "w")

nr_bins = len(bin_mids)

def predict_P_F_scores(P_score_F_refs, P_score_targets):
	P_F_score_preds = []
	for binidx in range(nr_bins):
		score = bin_mids[binidx]
		P_score_F_ref = P_score_F_refs[binidx]
		P_score_target = P_score_targets[binidx]

		P_F_score_Bayes = 0
		if P_score_target > 0:
			P_F_score_Bayes = Args.prior_pf*P_score_F_ref/P_score_target
			if P_F_score_Bayes > 1:
				P_F_score_Bayes = 1
		P_F_score_preds.append(P_F_score_Bayes)
	return np.array(P_F_score_preds, dtype=np.float32)

P_F_score_preds = predict_P_F_scores(P_score_F_refs, P_score_targets)
P_F_score_preds_smooth = smooth(P_F_score_preds, 7)

if not fout is None:
	s = "binmid"
	s += "\tP_score_target"
	s += "\tP_score_target_smooth"
	s += "\tP_score_F_ref"
	s += "\tP_F_score_target"
	s += "\tP_F_score_pred"
	s += "\tP_F_score_pred_smooth"
	fout.write(s + '\n')
	for binidx in range(nr_bins):
		score = bin_mids[binidx]
		P_F_score_target = P_F_score_targets[binidx]
		P_score_F_ref = P_score_F_refs[binidx]
		P_score_target = P_score_targets[binidx]
		P_score_target_smooth = P_score_targets_smooth[binidx]
		P_F_score_pred = P_F_score_preds[binidx]
		P_F_score_pred_smooth = P_F_score_preds_smooth[binidx]

		s = "%.3g" % score
		s += "\t%.3g" % P_score_target
		s += "\t%.3g" % P_score_target_smooth
		s += "\t%.3g" % P_score_F_ref
		s += "\t%.3g" % P_F_score_target
		s += "\t%.3g" % P_F_score_pred
		s += "\t%.3g" % P_F_score_pred_smooth
		fout.write(s + '\n')

if not Args.plot is None:
	fig, ax = plt.subplots(1, 1)
	ax.set_title("Bayes predict P_F_score\nref=%s\ntarget=%s" \
		% (Args.edf_ref, Args.edf_target))
	ax.set_xlabel("score")
	ax.set_ylabel("P_F_score")
	ax.set_yscale('log')
	if not xlim is None:
		ax.set_xlim(xlim)
	if not ylim is None:
		ax.set_ylim(ylim)

	ax.plot(bin_mids, P_F_score_refs, label = "ref", color = "lightgray")
	ax.plot(bin_mids, P_F_score_targets, label = "target", color = "blue")
	ax.plot(bin_mids, P_F_score_preds, label = "predicted", color = "magenta")
	ax.figure.set_size_inches(4.5, 3)
	fig.tight_layout()
	ax.legend()

	if not Args.plot is None:
		fig.savefig(Args.plot)
