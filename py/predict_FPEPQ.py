#!/usr/bin/python3

import re
import sys
import math
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from plot_dists_lib import read_dist

matplotlib.use('Agg')

AP = argparse.ArgumentParser()
AP.add_argument('--edf_ref', required=True)
AP.add_argument('--edf_target', required=True)
AP.add_argument('--target_prior_pf', type=float, default=0.5)
AP.add_argument('--output')
AP.add_argument('--evalues', default=False, action="store_true")
AP.add_argument('--obs_pf', default=False, action="store_true")
AP.add_argument('--plot', help="Plot file(s), default none")
AP.add_argument('--xrange', help="xlo,xhi")
AP.add_argument('--yrange', default="1e-2:100", help="ylo,yhi")
AP.add_argument('--loglin')
Args = AP.parse_args()

have_m_and_c = False
if Args.loglin:
	f = open(Args.loglin)
	line = f.readline()[:-1]
	M = re.search(r"m=(.+), c=(.+)", line)
	if M is None:
		assert False, "re failed '%s'\n" % line
	m = float(M.group(1))
	c = float(M.group(2))
	print("m=%.3g c=%.3g" % (m, c))
	have_m_and_c = True

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

def get_nq(edf_fn):
	for line in open(edf_fn):
		if not line.startswith('#'):
			continue
		M = re.search(r"qsize=(\d+)", line)
		if not M is None:
			return int(M.group(1))
	return None

def read_dist_dict(fn, name):
	global scores, nrbins, fn0
	scores_, dist = read_dist(fn, name)
	if scores is None:
		scores = scores_
		nrbins = len(scores)
		fn0 = fn
	else:
		if len(scores_) != len(scores) \
			or scores_[0] != scores[0] \
			or scores_[-1] != scores[-1]:
			sys.stderr.write(' '.join(sys.argv))
			sys.stderr.write("\n\nIncompatible scores %s, %s\n\n" % (fn, fn0))
			assert False
	dist_dict[name] = dist
	return dist

NQ_ref = get_nq(Args.edf_ref)
NQ_target = get_nq(Args.edf_target)

N_score_Fs_ref = read_dist_dict(Args.edf_ref, "N_score_F")
N_scores_target = read_dist_dict(Args.edf_target, "N_score")
N_scores_F_target = read_dist_dict(Args.edf_target, "N_score_F")
C_scores_F_ref = read_dist_dict(Args.edf_ref, "C_score_F")
FPEPQs_ref = read_dist_dict(Args.edf_ref, "cve_epq")
FPEPQs_target = read_dist_dict(Args.edf_target, "cve_epq")

fout = None
if not Args.output is None:
	fout = open(Args.output, "w")

NHF_ref = sum(N_score_Fs_ref)
NH_target = sum(N_scores_target)

NHF_target = sum(N_scores_F_target)
PF_target_obs = NHF_target/NH_target

def estimate_C(binidx):
	score = scores[binidx]
	logC = -(m*score + c)
	C = 10**logC
	if C > 1:
		C = 1
	return C

def estimate_FPEPQ_target_prior_PF(binidx):
	C = C_scores_F_ref[binidx]
	FPEPQ = Args.target_prior_pf*C*NH_target/NQ_target
	return FPEPQ

def estimate_FPEPQ_target_obs_PF(binidx):
	C = C_scores_F_ref[binidx]
	FPEPQ = PF_target_obs*C*NH_target/NQ_target
	return FPEPQ

def estimate_FPEPQ_target_prior_PF_mc(binidx):
	C = estimate_C(binidx)
	FPEPQ = Args.target_prior_pf*C*NH_target/NQ_target
	return FPEPQ

def estimate_FPEPQ_target_obs_PF_mc(binidx):
	C = estimate_C(binidx)
	FPEPQ = PF_target_obs*C*NH_target/NQ_target
	return FPEPQ

FPEPQs_target_pred_obsPF_old = []
FPEPQs_target_pred_priorPF_old = []
FPEPQs_target_pred_obsPF = []
FPEPQs_target_pred_priorPF = []
FPEPQs_target_pred_obsPF_mc = []
FPEPQs_target_pred_priorPF_mc = []
Cs = []
C_fits = []
for binidx in range(nrbins):
	FPEPQs_target_pred_priorPF.append(estimate_FPEPQ_target_prior_PF(binidx))
	FPEPQs_target_pred_obsPF.append(estimate_FPEPQ_target_obs_PF(binidx))
	if have_m_and_c:
		Cs.append(C_scores_F_ref[binidx])
		C_fits.append(estimate_C(binidx))
		FPEPQs_target_pred_priorPF_mc.append(estimate_FPEPQ_target_prior_PF_mc(binidx))
		FPEPQs_target_pred_obsPF_mc.append(estimate_FPEPQ_target_obs_PF_mc(binidx))

s = "score"
if Args.evalues:
	s += "\tE-value"
s += "\tFPEPQ_ref"
s += "\tFPEPQ_target"
s += "\tFPEPQ_target_pred_obsPF"
s += "\tFPEPQ_target_pred_priorPF"
if have_m_and_c:
	s += "\tC(score|F)"
	s += "\tC_fit"
	s += "\tFPEPQ_target_pred_obsPF_mc"
	s += "\tFPEPQ_target_pred_priorPF_mc"

if not fout is None:
	fout.write(s + '\n')

for binidx in range(nrbins):
	score = scores[binidx]
	s = "%.3g" % score
	if Args.evalues:
		s += "\t%.3g" % 10**(-score)
	s += "\t%.3g" % FPEPQs_ref[binidx]
	s += "\t%.3g" % FPEPQs_target[binidx]
	s += "\t%.3g" % FPEPQs_target_pred_obsPF[binidx]
	s += "\t%.3g" % FPEPQs_target_pred_priorPF[binidx]
	if have_m_and_c:
		s += "\t%.3g" % Cs[binidx]
		s += "\t%.3g" % C_fits[binidx]
		s += "\t%.3g" % FPEPQs_target_pred_obsPF_mc[binidx]
		s += "\t%.3g" % FPEPQs_target_pred_priorPF_mc[binidx]

	if not fout is None:
		fout.write(s + '\n')

	if FPEPQs_target[binidx] < 1e-4 \
		and FPEPQs_target[binidx] < 1e-4 \
		and FPEPQs_target_pred_obsPF[binidx] < 1e-4 \
		and FPEPQs_target_pred_priorPF[binidx] < 1e-4:
		break

def fixname(fn):
	name = fn
	name = name.replace("../edf/", "")
	name = name.replace("scop40", "")
	name = name.replace("..", ".")
	name = name.replace("..", ".")
	name = name.replace("..", ".")
	name = name.replace("sensitive_ts", "sts")
	name = name.replace("exhaustive", "ex")
	name = name.replace("default", "def")
	if name.endswith("."):
		name = name[:-1]
	return name

fig, ax = plt.subplots(1, 1)
name_ref = fixname(Args.edf_ref)
name_target = fixname(Args.edf_target)
ax.set_title("ref=%s\ntarget=%s" % (name_ref, name_target))
ax.set_xlabel("score")
ax.set_ylabel("FPEPQ")
ax.set_yscale('log')
if not xlim is None:
	ax.set_xlim(xlim)
if not ylim is None:
	ax.set_ylim(ylim)

ax.plot(scores, FPEPQs_target, label = "Measured", color="blue", linestyle="solid")
if Args.obs_pf:
	ax.plot(scores, FPEPQs_target_pred_obsPF, label = "Pred(obs PF)", color="magenta", linestyle="solid")

PF = Args.target_prior_pf
if PF == 1:
	pred_label = "Pred.(PF=1)"
elif PF == 0.5:
	pred_label = "Pred.(PF=0.5)"
else:
	pred_label = "Pred.(PF=%.2f)" % PF

ax.plot(scores, FPEPQs_target_pred_priorPF, label = pred_label, color="magenta", linestyle="dashed")

if have_m_and_c:
	ax.plot(scores, FPEPQs_target_pred_priorPF_mc, label = "Pred(prior+fit)", color="magenta", linestyle="dotted")

ax.plot(scores, FPEPQs_ref, label = "Ref", color = "lightgray", linestyle="dashdot")
ax.figure.set_size_inches(4.5, 3)
fig.tight_layout()
ax.legend()

if not Args.plot is None:
	fns = Args.plot.split(',')
	for fn in fns:
		sys.stderr.write(fn + '\n')
	fig.savefig(fn)

if not fout is None:
	fout.write("# " + ' '.join(sys.argv) + '\n')

fout.close()