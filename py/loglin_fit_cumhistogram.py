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
AP.add_argument("--hist", required=True, help="histogram TSV")
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

fout = None
if not Args.output is None:
	fout = open(Args.output, "w")

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

counts = []
scores = []
for line in open(Args.hist):
	if line.startswith('#'):
		continue
	flds = line[:-1].split('\t')

###################################################
# Special case for Foldseek first negative bitscore
# Artifact of integer score rounding?
	if Args.foldseek_outlier and flds[0] == "-0.4":
		flds[1] = "400000"
###################################################

	score = float(flds[0])
	count = int(flds[1])
	scores.append(score)
	counts.append(count)
minscore = scores[0]
maxscore = scores[-1]

nrbins = len(counts)
assert len(scores) == nrbins

scoresz = []
nsz = []

scores_to_fit = []
logns_to_fit = []
ns = []
n = 0
for binidx in range(nrbins-1, -1, -1):
	score = scores[binidx]
	n += counts[binidx]
	ns.append(n)
	if n > 0:
		scoresz.append(score)
		nsz.append(n)
		if score >= Args.fitlo and score <= Args.fithi:
			logn = math.log10(n)
			scores_to_fit.append(score)
			logns_to_fit.append(logn)
ns = ns[::-1]

m, c, r_value, p_value, std_err = \
	stats.linregress(scores_to_fit, logns_to_fit)


scores_fitz = []
nhats_fitz = []
for binidx in range(nrbins):
	score = scores[binidx]
	n = ns[binidx]
#	print(f"{score=} {n=}")
	if n > 0 and score >= Args.fitlo and score <= Args.fithi:
		scores_fitz.append(score)
		lognhat = m*score + c
		nhat = 10**lognhat
		nhats_fitz.append(nhat)
# print(f"{scores_fitz=} {nhats_fitz=}")

#######################################################################
# Draw dashed line showing extension of log-linear fit to higher scores
extend_score_lo = Args.fithi
extend_score_hi = xlim_log[1]
scores_extend = np.linspace(extend_score_lo, extend_score_hi, 10)
nhats_extend = []
for score in scores_extend:
	lognhat = m*score + c
	nhat = 10**lognhat
	nhats_extend.append(nhat)
#######################################################################

print("%10.4g  m" % m)
print("%10.4g  c" % c)

fout.write("%10.4g  m\n" % m)
fout.write("%10.4g  c\n" % c)

fig, ax = plt.subplots(1, 1)

ax.set_xlabel(Args.xlabel)
ax.set_ylabel("Accum. nr. hits")

ax.plot(scoresz, nsz,
	label = "Measured",
	color = "skyblue")

ax.plot(scores_fitz,
	nhats_fitz,
	label = "Log-linear fit",
	color = "black",
	linewidth = 2)

ax.plot(scores_extend,
	nhats_extend,
	color = "black",
	linestyle = "dotted",
	label = "Extrapolated fit",
	linewidth = 2)

ax.fill_between(scoresz, nsz, 0, color=Args.fill)

#################################################################
# Draw vertical lines bracketing range of scores used for fitting
lognhat = m*scores_fitz[0] + c
nhat = 10**lognhat
xs = [ Args.fitlo, Args.fitlo ]
ys = [ 0, nhat ]
vertline = matplotlib.lines.Line2D(xs, ys, color="black", linewidth=1, linestyle="dashed")
ax.add_line(vertline)

lognhat = m*scores_fitz[-1] + c
nhat = 10**lognhat
xs = [ Args.fithi, Args.fithi ]
ys = [ 0, nhat ]
vertline = matplotlib.lines.Line2D(xs, ys, color="black", linewidth=1, linestyle="dashed")
ax.add_line(vertline)
#################################################################

#################################################################
# Text showing fitted parameters
formula = "log10(n)=\n%.3g - %.3g*score" % (c, -m)
props = dict(boxstyle='round', 
			facecolor='whitesmoke',
			edgecolor="lightgray",
			alpha=0.8,
			pad=1)

textbox_x = (Args.fithi + Args.fitlo)/2
textbox_y = nhat
if not Args.textbox_x is None:
	textbox_x = Args.textbox_x
if not Args.textbox_y is None:
	textbox_y = Args.textbox_y
ax.text(textbox_x, textbox_y, formula,
		bbox = props,
		horizontalalignment='center',
		verticalalignment='center')
#################################################################

ax.legend()
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

fout.close()