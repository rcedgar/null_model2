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
AP.add_argument('--algo', required=True)
AP.add_argument('--targets', required=True)
AP.add_argument('--prior_pf', type=float, default=0.5)
AP.add_argument('--output')
AP.add_argument('--loscore', type=float, required=True)
AP.add_argument('--delta', type=float, required=True)
AP.add_argument('--nrscores', type=int, required=True)
AP.add_argument('--evalues', default=False, action="store_true")
AP.add_argument('--plot', help="Plot file(s), default no plot")
AP.add_argument('--xrange')
AP.add_argument('--xlabel')
AP.add_argument('--yrange', default="1e-3:100")
Args = AP.parse_args()

def read_m_c(fn):
	f = open(fn)
	line = f.readline()[:-1]
	M = re.search(r"m=(.+), c=(.+)", line)
	if M is None:
		assert False, "re failed '%s'\n" % line
	m = float(M.group(1))
	c = float(M.group(2))
	return m, c

standards = [ "scop40", "scop40c"]
mdict = {}
cdict = {}
mdict["scop40"], cdict["scop40"] = read_m_c("../fit_loglin/" + Args.algo + ".scop40.tsv")
mdict["scop40c"], cdict["scop40c"] = read_m_c("../fit_loglin/" + Args.algo + ".scop40c.tsv")

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

table_scores = []
score = Args.loscore
for i in range(Args.nrscores):
	table_scores.append(score)
	score += Args.delta

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

fout = None
if not Args.output is None:
	fout = open(Args.output, "w")

def estimate_C(score, m, c):
	logC = -(m*score + c)
	C = min(10**logC, 1)
	return C

def estimate_FPEPQ(score, m, c, NH_target, NQ_target):
	C = estimate_C(score, m, c)
	FPEPQ = Args.prior_pf*C*NH_target/NQ_target
	return FPEPQ

def do_target(target, m, c):
	edf_fn = "../edf/" + Args.algo + "." + target
	NQ_target = get_nq(edf_fn)
	_, N_scores_target = read_dist(edf_fn, "N_score")
	NH_target = sum(N_scores_target)
	N_scores_target = None
	FPEPQs = []
	for score in table_scores:
		FPEPQ = estimate_FPEPQ(score, m, c, NH_target, NQ_target)
		FPEPQs.append(FPEPQ)
	return FPEPQs

targets = Args.targets.split(',')
FPEPQs_dict = {}
for target in targets:
	for standard in standards:
		FPEPQs_dict[(target, standard)] \
			= do_target(target, mdict[standard], cdict[standard])

s = "score"
if Args.evalues:
	s += "\tE-value"
for target in targets:
	for standard in standards:
		s += "\t" + target + "/" + standard
if not fout is None:
	fout.write(s + '\n')

for idx in range(len(table_scores)):
	score = table_scores[idx]
	s = "%.3g" % score
	if Args.evalues:
		s += "\t%.3g" % (10**-score)
	for target in targets:
		for standard in standards:
			FPEPQ = FPEPQs_dict[(target, standard)][idx]
			if FPEPQ > 10:
				s += "\t>10"
			else:
				s += "\t%.3g" % FPEPQ
	if not fout is None:
		fout.write(s + '\n')
fout.close()

def get_style(target, standard):
	style = {}
	if standard == "scop40c":
		style["linestyle"] = "dotted"
	if target == "scop40_afdb50":
		style["color"] = "black"
		style["linewidth"] = 2
	elif target == "scop40":
		style["color"] = "dodgerblue"
	elif target == "scop40c":
		style["color"] = "lightskyblue"
	return style

def get_label(target, standard):
	if target == "scop40_afdb50":
		label = "AFDB50"
	elif target == "scop40":
		label = "SCOP40"
	elif target == "scop40c":
		return "SCOP40c"
	if standard == "scop40c":
		label += "/c"
	return label

fig, ax = plt.subplots(1, 1)
ax.set_title("Estimated E-values " + Args.algo)
if not Args.xlabel is None:
	ax.set_xlabel(Args.xlabel)
elif Args.evalues:
	ax.set_xlabel("Reported E-value")
else:
	ax.set_xlabel("score")

ax.set_ylabel("Estimated E-value")
ax.set_yscale('log')
if not xlim is None:
	ax.set_xlim(xlim)
if not ylim is None:
	ax.set_ylim(ylim)

for target in targets:
	for standard in standards:
		FPEPQs = FPEPQs_dict[(target, standard)]
		label = get_label(target, standard)
		ax.plot(table_scores, FPEPQs, label = label, **get_style(target, standard))

if Args.evalues:
	labels = []
	ticks = []
	for score in table_scores:
		E = 10**(-score)
		ticks.append(score)
		label = "%.2g" % E
		if label.startswith("1e"):
			label = "E" + label[2:]
		labels.append(label)
	if len(ticks) > 8:
		ticks = ticks[1::2]
		labels = labels[1::2]
	ax.set_xticks(ticks, labels)

ax.figure.set_size_inches(4.5, 3)
fig.tight_layout()
ax.legend()

if not Args.plot is None:
	fns = Args.plot.split(',')
	for fn in fns:
		sys.stderr.write(fn + '\n')
	fig.savefig(fn)
