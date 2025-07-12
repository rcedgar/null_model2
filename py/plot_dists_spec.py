#!/usr/bin/python3

import sys
import math
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from plot_dists_lib import read_dist

specfn = sys.argv[1]
svgfn = sys.argv[2]
pngfn = None
if len(sys.argv) > 3:
	pngfn = sys.argv[3]

edfdir = "../edf/"

matplotlib.use('Agg')

minscore = None
maxscore = None
evalues = False

edf_fns = []
edf_labels = []

distnames = []
titles = []
edf_fns = []
labels = []
colors = []
linestyles = []
ylim_logs = []
xlabel = None
ylabel = None
for line in open(specfn):
	line = line.strip()
	if line.startswith('#') or len(line) == 0:
		continue
	flds = line.split('\t')
	if flds[0] == "distname":
		assert len(flds) == 5
		distnames.append(flds[1])
		titles.append(flds[2])
		ylim_logs.append([ float(flds[3]), float(flds[4]) ])
	elif flds[0] == "axislabels":
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
	elif flds[0] == "edf":
		assert len(flds) == 5, flds
		edf_fns.append(flds[1])
		labels.append(flds[2])
		colors.append(flds[3])
		linestyles.append(flds[4])
	else:
		assert False, f"{flds=}"

nrdists = len(distnames)
nredfs = len(edf_fns)

fig, axs = plt.subplots(nrdists, 2)

assert not minscore is None
assert not maxscore is None
xlim = [minscore, maxscore]
def plot_dist(distidx):
	if nrdists == 1:
		axs_ = axs
	else:
		axs_ = axs[distidx]
	distname = distnames[distidx]
	title = titles[distidx]
	for logscale in [ False, True ]:
		if logscale:
			ax = axs_[1]
		else:
			ax = axs_[0]
		for edfidx in range(nredfs):
			edf_fn = edf_fns[edfidx]
			binmids, PDF = read_dist(edfdir + edf_fn, distname)
			ax.plot(binmids, PDF, \
				label = labels[edfidx], \
				color = colors[edfidx], \
				linestyle = linestyles[edfidx])
		ax.set_xlim(xlim)
		if logscale:
			ax.set_yscale('log')
			ax.set_ylim(ylim_logs[distidx])
			ax.set_title(title + " (logscale)")
		else:
			ax.set_title(title)
		ax.set_ylabel(ylabel)
		ax.set_xlabel(xlabel)
		ax.legend()

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

for distidx in range(nrdists):
	plot_dist(distidx)

set_size(8, 3*nrdists)
fig.suptitle(svgfn)
fig.tight_layout()
sys.stderr.write(svgfn + '\n')
fig.savefig(svgfn)

if not pngfn is None:
	sys.stderr.write(pngfn + '\n')
	fig.savefig(pngfn)
