#!/usr/bin/python3

import sys
import math
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from plot_dists_lib import read_dist

AP = argparse.ArgumentParser()
AP.add_argument("--plot", required=False, help="Plot file")
AP.add_argument("--logscale", default=False, action="store_true")
AP.add_argument("--specs", required=True, nargs='+')
AP.add_argument("--cols", type=int, default=2)
Args = AP.parse_args()

specfns = Args.specs

if len(specfns) == 1:
	Args.logscale = True

matplotlib.use('Agg')
edfdir = "../edf/"

def set_size(w, h, ax=None):
	""" w, h: width, height in inches """
	if not ax: ax=plt.gca()
	l = ax.figure.subplotpars.left
	r = ax.figure.subplotpars.right
	t = ax.figure.subplotpars.top
	b = ax.figure.subplotpars.bottom
	figw = float(w)/(r-l)
	figh = float(h)/(t-b)
	ax.figure.set_size_inches(figw, figh)

def plot_spec(ax_lin, ax_log, specfn):
	minscore = None
	maxscore = None
	evalues = False

	edf_fns = []
	edf_labels = []

	distname = None
	title = None
	edf_fns = []
	labels = []
	colors = []
	linestyles = []
	xlabel = None
	ylabel = None
	ylim_lin = None
	ylim_log = None
	for line in open(specfn):
		line = line.strip()
		if line.startswith('#') or len(line) == 0:
			continue
		flds = line.split('\t')
		if flds[0] == "distname":
			assert len(flds) >= 3
			assert distname is None
			distname = flds[1]
			title = flds[2]
		elif flds[0] == "axislabels":
			assert len(flds) == 3
			xlabel = flds[1]
			ylabel = flds[2]
		elif flds[0] == "evalues":
			assert len(flds) == 2
			evalues = True
		elif flds[0] == "minscore":
			assert len(flds) == 2
			minscore = float(flds[1])
		elif flds[0] == "maxscore":
			assert len(flds) == 2
			maxscore = float(flds[1])
		elif flds[0] == "yrange":
			assert len(flds) == 5
			ylim_lin = [ float(flds[1]), float(flds[2]) ]
			ylim_log = [ float(flds[3]), float(flds[4]) ]
		elif flds[0] == "edf":
			assert len(flds) == 5, flds
			edf_fns.append(flds[1])
			labels.append(flds[2])
			colors.append(flds[3])
			linestyles.append(flds[4])
		else:
			assert False, f"{flds=}"

	nredfs = len(edf_fns)

	assert not minscore is None
	assert not maxscore is None
	xlim = [minscore, maxscore]
	nredfs = len(edf_fns)
	for edfidx in range(nredfs):
		edf_fn = edf_fns[edfidx]
		binmids, PDF = read_dist(edfdir + edf_fn, distname)
		ax_lin.plot(binmids, PDF, \
			label = labels[edfidx], \
			color = colors[edfidx], \
			linestyle = linestyles[edfidx])

		if not ax_log is None:
			ax_log.plot(binmids, PDF, \
				label = labels[edfidx], \
				color = colors[edfidx], \
				linestyle = linestyles[edfidx])

	ax_lin.set_xlabel(xlabel)
	ax_lin.set_ylabel(ylabel)
	ax_lin.set_xlim(xlim)
	if not ylim_lin is None:
		ax_lin.set_ylim(ylim_lin)
	ax_lin.set_title(title)
	ax_lin.legend()

	if not ax_log is None:
		ax_log.set_xlabel(xlabel)
		ax_log.set_ylabel(ylabel)
		ax_log.set_xlim(xlim)
		if not ylim_log is None:
			ax_log.set_ylim(ylim_log)
		ax_log.set_title(title + " logscale")
		ax_log.set_yscale('log')
		ax_log.legend()

n = len(specfns)
cols = Args.cols
if Args.logscale:
	assert cols%2 == 0
	rows = n//(cols//2)
else:
	assert n%cols == 0
	rows = n//cols
print("rows=", rows, "cols=", cols)

fig, axs = plt.subplots(rows, cols)

col = 0
row = 0
for idx in range(n):
	if rows > 1:
		lin_ax = axs[row][col]
		if Args.logscale:
			log_ax = axs[row][col+1]
	else:
		lin_ax = axs[col]
		if Args.logscale:
			log_ax = axs[col+1]

	if Args.logscale:
		row = (2*idx)//cols
		col = (2*idx)%cols
		print("idx=", idx, "row=", row, "col=", col)
		plot_spec(lin_ax, log_ax, specfns[idx])
		col += 2
	else:
		row = idx//cols
		col = idx%cols
		plot_spec(lin_ax, None, specfns[idx])
		col += 1
	if col > cols:
		assert False, "col=%d cols=%d" % (col, cols)
	if col == cols:
		col = 0
		row += 1

set_size(3*cols, 2.5*rows)
fig.tight_layout()

if not Args.plot is None:
	fns = Args.plot.split(',')
	for fn in fns:
		sys.stderr.write(fn + '\n')
		fig.savefig(fn)
