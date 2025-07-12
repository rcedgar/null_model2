#!/usr/bin/python3

import sys
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from plot_dists_lib import read_dist

AP = argparse.ArgumentParser()
AP.add_argument("--edfs", required=True, nargs='+')
AP.add_argument("--labels", required=True, nargs='+')
AP.add_argument("--colors")
AP.add_argument("--plot", nargs="*")
AP.add_argument("--title")
AP.add_argument("--minscore", type=float, default=-1)
AP.add_argument("--maxscore", type=float, default=10)
AP.add_argument('--xrange', help="xlo,xhi")
AP.add_argument('--yrange', default="1e-3:10")
Args = AP.parse_args()

# value 0..1
def get_viridis_color(value):
	colormap = plt.cm.viridis
	color = colormap(value)
	r, g, b, _ = color  # Discard the alpha channel
	return (r, g, b)

ideal_color = get_viridis_color(0.9)
ideal_linestyle = "dashed"

matplotlib.use('Agg')

edffns = Args.edfs
labels = Args.labels
colors = [ get_viridis_color(0), get_viridis_color(0.5) ]
if not Args.colors is None:
	colors = Args.colors.split(',')

N = len(edffns)
assert len(labels) == N

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

fig, ax = plt.subplots(1, 1)

ax.set_xlabel("Reported E-value")
ax.set_ylabel("Measured FPEPQ")

for idx in range(N):
	epqs = []
	evalues = []
	ideals = []
	scores, cve_epqs = read_dist(edffns[idx], "cve_epq")
	for score in range(Args.minscore, Args.maxscore+1):
		epq = np.interp(score, scores, cve_epqs)
		evalue = 10**(-score)
		epqs.append(epq)
		evalues.append(evalue)
		ideals.append(evalue)
	ax.plot(evalues, epqs, label=labels[idx])

ax.plot(ideals, ideals, label="Ideal E-value", \
	color=ideal_color, linestyle=ideal_linestyle)

ax.legend()
ax.set_xscale('log')
ax.set_yscale('log')
if not Args.title is None:
	ax.set_title(Args.title)
if not xlim is None:
	ax.set_xlim(xlim)
if not ylim is None:
	ax.set_ylim(ylim)

set_size(4, 3)
fig.tight_layout()
if not Args.plot is None:
	for fn in Args.plot:
		sys.stderr.write(fn + '\n')
		fig.savefig(fn)
