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

prior_pf = 0.5

algos		= [	"dali",		"tm",	"foldseek",	"reseek_fast"	]
titles		= [	"DALI",		"TM-align",	"Foldseek",	"Reseek (fast)"	]
areEs		= [ False,		False,	True,		True			]
loscores	= [	2,			0.2,	-1,			-1				]	
deltas		= [	2,			0.1,	1,			1				]	
nrscores	= [	20,			9,		14,			8				]	
xlos		= [	2,			0.3,	-1,			-1				]	
xhis		= [	40,			1.0,	12,			6				]	
ylos		= [	1e-5,		1e-3,	1e-3,		1e-3			]	
yhis		= [	10,			10,		10,			10				]
AFDB_scales	= [	1000,		1000,	None,		None			]
xlabels		= [	"Z score",	"TM score",	"Reported E-value", "Reported E-value"	]

def get_targets(algo):
	if algo == "dali" or algo == "tm":
		targets = [ "scop40", "afdb_scaled" ]
	elif algo == "foldseek" or algo == "reseek_fast":
		targets = [ "scop40", "scop40_afdb50" ]
	else:
		assert False, "algo=" + algo
	return targets

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

fig, axs = plt.subplots(2, 2)

def get_nq(edf_fn):
	for line in open(edf_fn):
		if not line.startswith('#'):
			continue
		M = re.search(r"qsize=(\d+)", line)
		if not M is None:
			return int(M.group(1))
	return None

def estimate_C(score, m, c):
	logC = -(m*score + c)
	C = min(10**logC, 1)
	return C

def estimate_FPEPQ(score, m, c, NH_target, NQ_target):
	C = estimate_C(score, m, c)
	FPEPQ = prior_pf*C*NH_target/NQ_target
	return FPEPQ

def get_style(target, standard):
	style = {}
	if standard == "scop40c":
		style["linestyle"] = "dashed"
	if target == "scop40_afdb50":
		style["color"] = "black"
	elif target == "afdb_scaled":
		style["color"] = "blue"
	elif target == "scop40":
		style["color"] = "orchid"
	else:
		sys.stderr.write("get_style(%s, %s)\n" % (target, standard))
		assert False
	return style

def get_label(target, standard):
	if target == "scop40_afdb50":
		label = "AFDB50"
	elif target == "afdb_scaled":
		label = "AFDB50(scaled)"
	elif target == "scop40":
		label = "SCOP40"
	elif target == "scop40c":
		return "SCOP40c"
	if standard == "scop40c":
		label += "/c"
	return label

def do_target(algo, target, m, c, table_scores):
	if target == "afdb_scaled":
		edf_fn = "../edf/" + algo + ".scop40"
	else:
		edf_fn = "../edf/" + algo + "." + target
	NQ_target = get_nq(edf_fn)
	_, N_scores_target = read_dist(edf_fn, "N_score")
	NH_target = sum(N_scores_target)
	N_scores_target = None
	FPEPQs = []
	for score in table_scores:
		FPEPQ = estimate_FPEPQ(score, m, c, NH_target, NQ_target)
		FPEPQs.append(FPEPQ)
	return FPEPQs

def get_evalue_tick_label_from_score(score):
	i = round(score)
	if i == -2:
		return "100"
	if i == -1:
		return "10"
	if i == 0:
		return "1"
	if i == 1:
		return "0.1"
	if i == 2:
		return "0.01"
	return "E-%02d" % i

def do_algo(idx):
	row = idx//2
	col = idx%2
	ax = axs[row][col]
	algo = algos[idx]
	title = titles[idx]
	is_evalue = areEs[idx]
	loscore = loscores[idx]
	delta = deltas[idx]
	nrs = nrscores[idx]
	xlo = xlos[idx]
	xhi = xhis[idx]
	ylo = ylos[idx]
	yhi = yhis[idx]
	xlabel = xlabels[idx]
	AFDB_scale = AFDB_scales[idx]

	mdict = {}
	cdict = {}
	mdict["scop40"], cdict["scop40"] = read_m_c("../fit_loglin/" + algo + ".scop40.tsv")
	mdict["scop40c"], cdict["scop40c"] = read_m_c("../fit_loglin/" + algo + ".scop40c.tsv")

	xlim = [ xlo, xhi ]
	ylim = [ ylo, yhi ]

	table_scores = []
	score = loscore
	for i in range(nrs):
		table_scores.append(score)
		score += delta

	scores = None
	nrbins = None
	dist_dict = {}

	targets = get_targets(algo)
	FPEPQs_dict = {}
	for target in targets:
		for standard in standards:
			FPEPQs_dict[(target, standard)] \
				= do_target(algo, target, mdict[standard], cdict[standard], table_scores)

	ax.set_title(title)
	ax.set_xlabel(xlabel)

	ax.set_ylabel("Estimated E-value")
	ax.set_yscale('log')
	ax.set_xlim(xlim)
	ax.set_ylim(ylim)

	for target in targets:
		for standard in standards:
			FPEPQs = FPEPQs_dict[(target, standard)]
			if target == "afdb_scaled":
				for i in range(len(FPEPQs)):
					FPEPQs[i] *= AFDB_scale
			label = get_label(target, standard)
			ax.plot(table_scores, FPEPQs, label = label, **get_style(target, standard))

	ticks = []
	labels = []

	ts =	[ 1e-5,		1e-4,	1e-3,	1e-2,	1e-1,	1e0,	1e1,	1e2 ]
	labs = [ "E-5",	"E-4",	"E-3",	"0.01",	"0.1",	"1",	"10",	"100" ]

	for k in range(len(ts)):
		t = ts[k]
		if t >= ylo and t <= yhi:
			ticks.append(t)
			labels.append(labs[k])
	ax.set_yticks(ticks, labels)

	if algo == "reseek_fast" or algo == "foldseek":
		labels = []
		ticks = []
		for score in table_scores:
			label = get_evalue_tick_label_from_score(score)
			ticks.append(score)
			labels.append(label)
		if len(ticks) > 8:
			ticks = ticks[1::2]
			labels = labels[1::2]
		ax.set_xticks(ticks, labels)

		xs = [ -math.log10(ylo), -math.log10(yhi) ]
		ys = [ ylo, yhi ]
		ideal_color = "limegreen"
		ideal_linestyle = "dashdot"
		ideal_line = matplotlib.lines.Line2D(xs, ys, \
			color=ideal_color, linestyle=ideal_linestyle)
		ax.add_line(ideal_line)
		handles, labels = ax.get_legend_handles_labels()
		handles.append(plt.Line2D([0], [0], \
			color=ideal_color, linestyle=ideal_linestyle))
		labels.append('Ideal')
		ax.legend(handles, labels)
	else:
		ax.legend()


	ax.invert_xaxis()

for algo_idx in range(len(algos)):
	do_algo(algo_idx)

fig.set_size_inches(9, 6)
fig.tight_layout()
fn = "../results/estimated_evalues_figure.svg"
sys.stderr.write(fn + '\n')
fig.savefig(fn)
