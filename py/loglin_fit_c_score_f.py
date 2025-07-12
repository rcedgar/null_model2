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
AP.add_argument("--plot", help="Plot file")
AP.add_argument("--output", help="TSV output file")
AP.add_argument("--title")
AP.add_argument('-x', "--xlabel", default="Score")
AP.add_argument("--fitlo", type=float, required=True)
AP.add_argument("--fithi", type=float, required=True)
AP.add_argument('--xrange', type=str, required=True, help="xlo:xhi")
AP.add_argument('--yrange', type=str, default="1e-4:1", help="ylo:yhi")
AP.add_argument('--textbox_x', type=float)
AP.add_argument('--textbox_y', type=float, default=0.1)
AP.add_argument("--fill", default='powderblue')
AP.add_argument("--prob", default=False, action="store_true")
AP.add_argument('--foldseek_outlier', default=False, action="store_true", 
				help="Fix anomalous bin")
Args = AP.parse_args()

if Args.prob:
	distname = "P_score_F"
else:
	distname = "C_score_F"

fout = None
if not Args.output is None:
	fout = open(Args.output, "w")

flds = Args.xrange.replace('_', '-').split(':')
assert len(flds) == 2
xlim_log = [ float(flds[0]), float(flds[1]) ]

flds = Args.yrange.replace('_', '-').split(':')
assert len(flds) == 2
ylim_log = [ float(flds[0]), float(flds[1]) ]

def read_dist(fn, distname):
	bin_mids = []
	fld_nr = None
	v = []
	for line in open(fn):
		if line.startswith('#'):
			continue
		if fld_nr is None:
			hdr = line[:-1].split('\t')
			assert hdr[0] == "binmids"
			for i in range(len(hdr)):
				if hdr[i] == distname:
					fld_nr = i
					break
			if fld_nr is None:
				assert False, "distname=%s not found in fn=%s" % (distname, fn)
			continue
		if len(line.strip()) == 0:
			continue
		flds = line[:-1].split('\t')
		bin_mid = float(flds[0])
		x = float(flds[fld_nr])

		bin_mids.append(bin_mid)
		v.append(x)
	return bin_mids, v

bin_mids, C_score_F = read_dist(Args.edf, distname)
nrbins = len(bin_mids)
assert len(C_score_F) == nrbins

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

scores = []
Ps = []

for binidx in range(nrbins):
	score = bin_mids[binidx]
	P = C_score_F[binidx]
	if P > 1e-4:
		scores.append(score)
		Ps.append(P)

nrbinsz = len(scores)

scores_to_fit = []
logPs_to_fit = []

for binidx in range(nrbinsz):
	score = scores[binidx]
	if score < Args.fitlo or score > Args.fithi:
		continue
	P = C_score_F[binidx]
	if P > 1e-4 and score >= Args.fitlo and score <= Args.fithi:
		logP = -math.log10(P)
		scores_to_fit.append(score)
		logPs_to_fit.append(logP)

m, c, r_value, p_value, std_err = \
	stats.linregress(scores_to_fit, logPs_to_fit)

s = "m=%.4g, c=%.4g" % (m, c)

sys.stderr.write(s + '\n')
fout.write(s + '\n')

fig, ax = plt.subplots(1, 1)

ax.set_xlabel(Args.xlabel)
if Args.prob:
	ax.set_ylabel("P(score|F)")
else:
	ax.set_ylabel("CDF(score|F)")

ax.plot(scores, Ps, label = "Measured", color = "skyblue")
ax.fill_between(scores, Ps, 0, color=Args.fill)

#################################################################
# Draw vertical lines bracketing range of scores used for fitting
logPhat_lo = -(m*scores_to_fit[0] + c)
Phat_lo = 10**logPhat_lo

xlo = scores_to_fit[0] 
xhi = scores_to_fit[-1]

xs = [ xlo, xlo ]
ys = [ 0, Phat_lo ]
vertline = matplotlib.lines.Line2D(xs, ys, color="black", linewidth=1, linestyle="dashed")
ax.add_line(vertline)

logPhat_hi = -(m*scores_to_fit[-1] + c)
Phat_hi = 10**logPhat_hi
xs = [ xhi, xhi ]
ys = [ 0, Phat_hi ]
vertline = matplotlib.lines.Line2D(xs, ys, color="black", linewidth=1, linestyle="dashed")
ax.add_line(vertline)

xs = [ xlo, xhi ]
ys = [ Phat_lo, Phat_hi ]
fitline = matplotlib.lines.Line2D(xs, ys, color="black", linewidth=2, linestyle="solid")
ax.add_line(fitline)
#################################################################

#################################################################
# Text showing fitted parameters
formula = "-log10(CDF)=\n%.3g + %.3g*score" % (c, m)
props = dict(boxstyle='round', 
			facecolor='whitesmoke',
			edgecolor="lightgray",
			alpha=0.8,
			pad=1)

textbox_x = xlim_log[1] - (xlim_log[1] - xlim_log[0])/8
textbox_y = 1e-2
if not Args.textbox_x is None:
	textbox_x = Args.textbox_x
if not Args.textbox_y is None:
	textbox_y = Args.textbox_y
ax.text(textbox_x, textbox_y, formula,
		bbox = props,
		horizontalalignment='right',
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
	fns = Args.plot.split(',')
	for fn in fns:
		sys.stderr.write(fn + '\n')
		fig.savefig(fn)

fout.close()