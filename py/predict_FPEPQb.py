#!/usr/bin/python3

import re
import sys
import math
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from plot_dists_lib import read_dist
from bayes_evalue import estimate_FPEPQ, estimate_PF, estimate_h
from dbname2size import dbname2size

matplotlib.use('Agg')

AP = argparse.ArgumentParser()
AP.add_argument('--edfs', required=True, nargs='+')
AP.add_argument('--colors', required=True, type=int, nargs='+')
AP.add_argument('--labels', required=True, nargs='+')
AP.add_argument('--evalues', default=False, action="store_true")
AP.add_argument('--plot', help="Plot file(s), default none", nargs='+')
AP.add_argument('--xrange', help="xlo,xhi")
AP.add_argument('--yrange', default="1e-2:100", help="ylo,yhi")
AP.add_argument('--title')
AP.add_argument('--xlabel', default="score")
AP.add_argument('--output')
Args = AP.parse_args()

# value 0..100
def get_viridis_color(value):
	colormap = plt.cm.viridis
	color = colormap(value/100)
	r, g, b, _ = color  # Discard the alpha channel
	return (r, g, b)

fout = None
if not Args.output is None:
	fout = open(Args.output, "w")
	s = "score"
	if Args.evalues:
		s += "\tE-value"
	s += "\tFPEPQ_pred"
	fout.write(s + '\n')

evalues = Args.evalues

fig, ax = plt.subplots(1, 1)

def parse_edffn(edffn):
	name = edffn.split('/')[-1]
	flds = name.split('.')
	assert len(flds) == 4
	algo = flds[0].split('_')[0]
	q = flds[1]
	db = flds[2]
	ref = flds[3]
	dbsize = dbname2size[db]
	return algo, q, db, dbsize

for idx in range(len(Args.edfs)):
	edf = Args.edfs[idx]
	color = get_viridis_color(Args.colors[idx])
	label = Args.labels[idx]
	algo, q, db, dbsize = parse_edffn(edf)

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

	scores, FPEPQs = read_dist("../edf/" + edf, "cve_epq")
	nrbins = len(scores)

	h = estimate_h(algo, q, db)
	PF = estimate_PF(algo)

	FPEPQ_preds = []
	for binidx in range(nrbins):
		score = scores[binidx]
		FPEPQ = FPEPQs[binidx]
		FPEPQ_pred = estimate_FPEPQ(algo, "scop40", score, dbsize, PF, h)
		FPEPQ_preds.append(FPEPQ_pred)

	for binidx in range(nrbins):
		s = "%.3g" % scores[binidx]
		if Args.evalues:
			s += "\t%.3g" % 10**(-score)
		s += "\t%.3g" % FPEPQs[binidx]
		s += "\t%.3g" % FPEPQ_preds[binidx]
		if not fout is None:
			fout.write(s + '\n')


	ax.plot(scores, FPEPQs, label=label, color=color, linestyle="solid")
	ax.plot(scores, FPEPQ_preds, color=color, linestyle="dotted")

if not Args.title is None:
	ax.set_title(Args.title)
ax.set_ylabel("FPEPQ")
ax.set_yscale('log')
if not xlim is None:
	ax.set_xlim(xlim)
if not ylim is None:
	ax.set_ylim(ylim)

if xlim is None:
	xlo = min(scores)
	xhi = max(scores)
else:
	xlo, xhi = xlim

xlo = round(xlo)
xhi = round(xhi)

xlabel = Args.xlabel
if evalues:
	xlabel = "Reported E-value"
	xsteps = []
	xlabels = []
	stride = (xhi + 1 - xlo)//4
	if stride == 0:
		stride = 1
	for x in range(xlo, xhi+1, stride):
		xsteps.append(x)
		xlabels.append("%.1g" % (10**(-x)))
	ax.set_xticks(xsteps, xlabels)

ax.set_xlabel(xlabel)
ax.figure.set_size_inches(4.5, 3)
fig.tight_layout()
ax.legend()

if not Args.plot is None:
	for fn in Args.plot:
		sys.stderr.write(fn + '\n')
		fig.savefig(fn)

if not fout is None:
	fout.write("# " + ' '.join(sys.argv) + '\n')
	fout.close()
