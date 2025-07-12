#!/usr/bin/python3

import sys
import math
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from scipy import stats

matplotlib.use('Agg')

AP = argparse.ArgumentParser()
AP.add_argument("--edf", required=True)
AP.add_argument("--dist", required=True)
AP.add_argument("--plot", help="Plot file")
AP.add_argument("--output", help="TSV output file")
AP.add_argument("--title")
AP.add_argument("--xlabel", default="Score")
AP.add_argument("--fitlo", type=float, required=True)
AP.add_argument("--fithi", type=float, required=True)
AP.add_argument("--minscore", type=float)
AP.add_argument("--maxscore", type=float)
AP.add_argument('--xrange', type=str, required=True, help="xlo:xhi")
AP.add_argument('--yrange', type=str, required=True, help="ylo:yhi")
AP.add_argument('--textbox_x', type=float)
AP.add_argument('--textbox_y', type=float)
AP.add_argument("--fill", default='powderblue')
AP.add_argument('--foldseek_outlier', default=False, action="store_true", 
				help="Fix anomalous bin")
Args = AP.parse_args()

flds = Args.xrange.replace('_', '-').split(':')
assert len(flds) == 2
xlim_log = [ float(flds[0]), float(flds[1]) ]

flds = Args.yrange.replace('_', '-').split(':')
assert len(flds) == 2
ylim_log = [ float(flds[0]), float(flds[1]) ]

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

fld_nr = None
scores = []
values = []
for line in open(Args.edf):
	if line.startswith('#'):
		continue
	if fld_nr is None:
		hdr = line[:-1].split('\t')
		assert hdr[0] == "binmids"
		for i in range(len(hdr)):
			if hdr[i] == Args.dist:
				fld_nr = i
				break
		if fld_nr is None:
			assert False, "dist '%s' not found in fn=%s" % (Args.dist, fn)
		continue
	if len(line.strip()) == 0:
		continue
	flds = line[:-1].split('\t')
	bin_mid = float(flds[0])
	x = float(flds[fld_nr])

	scores.append(bin_mid)
	values.append(x)

nrbins = len(values)
assert len(scores) == nrbins

scoresz = []
valuesz = []

scores_to_fit = []
logns_to_fit = []
ns = []
for binidx in range(nrbins):
	score = scores[binidx]
	value = values[binidx]
	ns.append(value)
	if value > 0:
		scoresz.append(score)
		valuesz.append(value)
		if score >= Args.fitlo and score <= Args.fithi:
			logn = math.log10(value)
			scores_to_fit.append(score)
			logns_to_fit.append(logn)

m, c, r_value, p_value, std_err = \
	stats.linregress(scores_to_fit, logns_to_fit)

print("m=%.4g c=%.4g" % (m, c))
if not Args.output is None:
	fout = open(Args.output, "w")
	fout.write("m=%.4g c=%.4g\n" % (m, c))
	fout.close()

fig, ax = plt.subplots(1, 1)

name = Args.dist.replace('_', '(', 1)
name = name.replace('_', '|', 1)
name = name + ')'

ax.set_xlabel(Args.xlabel)
ax.set_ylabel(name)

ax.plot(scoresz, valuesz,
	label = "Measured",
	color = "skyblue")

ax.fill_between(scoresz, valuesz, 0, color=Args.fill)

#################################################################
# Line showing fit
nhat_lo = 10**(m*Args.fitlo + c)
nhat_hi = 10**(m*Args.fithi + c)

xs = [ Args.fitlo, Args.fithi ]
ys = [ nhat_lo, nhat_hi]
vertline = matplotlib.lines.Line2D(xs, ys, color="black", linewidth=2, linestyle="dashed")
ax.add_line(vertline)
#################################################################

#################################################################
# Text showing fitted parameters
formula = "log10(P)=\n%.3g - %.3g*score" % (c, -m)
props = dict(boxstyle='round', 
			facecolor='whitesmoke',
			edgecolor="lightgray",
			alpha=0.8,
			pad=1)

textbox_x = (Args.fithi + Args.fitlo)/2
textbox_y = (nhat_lo + nhat_hi)/2
if not Args.textbox_x is None:
	textbox_x = Args.textbox_x
if not Args.textbox_y is None:
	textbox_y = Args.textbox_y
ax.text(textbox_x, textbox_y, formula,
		bbox = props,
		horizontalalignment='left',
		verticalalignment='center')
#################################################################

# ax.legend()
ax.set_yscale('log')
if not xlim_log is None:
	ax.set_xlim(xlim_log)
if not ylim_log is None:
	ax.set_ylim(ylim_log)

if not Args.title is None:
	ax.set_title(Args.title.replace("\\n", "\n"))
set_size(4, 2.5)
# fig.suptitle(Args.plot)
fig.tight_layout()
if not Args.plot is None:
	sys.stderr.write(Args.plot + '\n')
	fig.savefig(Args.plot)
