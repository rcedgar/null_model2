#!/usr/bin/python3

import sys
import math
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from pymoo.algorithms.soo.nonconvex.pattern import PatternSearch
from pymoo.optimize import minimize
from pymoo.core.problem import Problem
import matplotlib.ticker as mticker

matplotlib.use('Agg')

AP = argparse.ArgumentParser()
AP.add_argument("--hist", required=True, help="histogram TSV")
AP.add_argument("--plot", required=False, help="Plot file(s)", nargs='+')
AP.add_argument("--output", required=False, help="TSV output file")
AP.add_argument("--title", required=False, help="Plot title")
AP.add_argument("--minscore", type=float, required=False)
AP.add_argument("--maxscore", type=float, required=False)
AP.add_argument('--xrange_lin', type=str, required=False, help="xlo,xhi")
AP.add_argument('--yrange_lin', type=str, required=False, help="ylo,yhi")
AP.add_argument('--xrange_log', type=str, required=False, help="ylo,yhi")
AP.add_argument('--yrange_log', type=str, required=False, help="ylo,yhi")
AP.add_argument('--barwlin', type=float, default=1.5)
AP.add_argument('--barwlog', type=float, default=1.2)
AP.add_argument('--plot_w', type=float, default=7)
AP.add_argument('--plot_h', type=float, default=2.5)
AP.add_argument('--textbox_x', type=float)
AP.add_argument('--textbox_y', type=float)
AP.add_argument('--foldseek_init', default=False, action="store_true")
AP.add_argument('--blastp_init', default=False, action="store_true")
AP.add_argument('--show_textbox', default=False, action="store_true")
AP.add_argument('--nofilename', default=False, action="store_true")
AP.add_argument("--xlabel", default="Score")
AP.add_argument("--init")
AP.add_argument('--foldseek_outlier', default=False, action="store_true", 
				help="Fix anomalous bin")
Args = AP.parse_args()

xlim_lin = None
if not Args.xrange_lin is None:
	flds = Args.xrange_lin.replace('_', '-').split(':')
	assert len(flds) == 2
	xlim_lin = [ float(flds[0]), float(flds[1]) ]
ylim_lin = None
if not Args.yrange_lin is None:
	flds = Args.yrange_lin.replace('_', '-').split(':')
	assert len(flds) == 2
	ylim_lin = [ float(flds[0]), float(flds[1]) ]

xlim_log = None
if not Args.xrange_log is None:
	flds = Args.xrange_log.replace('_', '-').split(':')
	assert len(flds) == 2
	xlim_log = [ float(flds[0]), float(flds[1]) ]
ylim_log = None
if not Args.yrange_log is None:
	flds = Args.yrange_log.replace('_', '-').split(':')
	assert len(flds) == 2
	ylim_log = [ float(flds[0]), float(flds[1]) ]

scores = []
scoresz = []
ns = []
nsz = []
modal_score = None
maxcount = 0
K = 0
for line in open(Args.hist):
	if line.startswith('#'):
		continue
	flds = line[:-1].split('\t')

###################################################
# Special case for Foldseek first negative bitscore
# Artifact of integer score rounding?
	if Args.foldseek_outlier and flds[0] == "-0.1":
		flds[1] = "400000"
###################################################

	score = float(flds[0])
	n = int(flds[1])
	K += score*n
	if n > maxcount:
		modal_score = score
		maxcount = n
	scores.append(score)
	ns.append(n)
	if n > 0:
		scoresz.append(score)
		nsz.append(n)
mean_score = K/sum(ns)

nrbins = len(ns)
dx = scores[1] - scores[0]
# assert scores increasing at constant intervals
WarningDone = False
for binidx in range(1, nrbins):
	thisdx = scores[binidx] - scores[binidx-1]
	assert thisdx > 0
	if thisdx/dx < 0.99 or thisdx/dx > 1.01:
		if not WarningDone:
			sys.stderr.write("WARNING [%d] %.3g %.3g dx=%.3g thisdx=%.3g\n" \
				% (binidx, scores[binidx-1], scores[binidx], dx, thisdx))
			WarningDone = True

# https://en.wikipedia.org/wiki/Gumbel_distribution
def Gumbel(mu, beta, x):
	z = float(x - mu)/beta
	try:
		e_z = math.exp(-z)
	except:
		e_z = None
	if e_z is None:
		return 0
	PDF = (1.0/beta)*math.exp(-(z + e_z))
	return PDF

minscore = scores[0]
maxscore = scores[-1]
lam = 0.57721
initial_mu = modal_score
initial_beta = abs((mean_score - modal_score)/lam)
ymu = Gumbel(initial_mu, initial_beta, initial_mu)
initial_norm = maxcount/ymu

def rmse(mu, beta, norm, center):
	d = 0
	for binidx in range(nrbins):
		score = scores[binidx]
		if not Args.minscore is None and score < Args.minscore:
			continue
		if not Args.maxscore is None and score > Args.maxscore:
			continue
		n = ns[binidx]
		if n == 0:
			continue
		y = Gumbel(mu, beta, score - center)
		nhat = norm*y
		dn = nhat - n
		d += dn**2
	return math.sqrt(d)

algorithm = PatternSearch()
scorerange = maxscore - minscore

# mu, beta, norm, center
if not Args.init is None:
	flds = Args.init.split(',')
	assert len(flds) == 8
	xls = []
	xus = []
	for i in range(4):
		xls.append(float(flds[2*i]))
		xus.append(float(flds[2*i+1]))

elif Args.foldseek_init:
	xls = [	initial_mu/10,	initial_beta/10,	initial_norm/10,	-100 ]
	xus = [	initial_mu/10,	initial_beta*10,	initial_norm*10,	100	]
else:
	xls = [	initial_mu/10,	initial_beta/10,	initial_norm/10,	-scorerange ]
	xus = [	initial_mu*10,	initial_beta*10,	initial_norm*10,	scorerange	]

rmse_initial = rmse(initial_mu, initial_beta, initial_norm, 0)

class FitGumbel(Problem):
	def __init__(self):
		# vars: mu, beta, norm, center
		super().__init__(n_var=4,
				   n_obj=1,
				   n_constr=0,
				   xl = xls,
				   xu = xus)

	def _evaluate(self, x, out, *args, **kwargs):
		n = len(x)
		ys = []
		for i in range(n):
			assert len(x[i]) == 4
			mu = x[i][0]
			beta = x[i][1]
			norm = x[i][2]
			center = x[i][3]
			y = rmse(mu, beta, norm, center)
			ys.append(y)
		out["F"] = ys

problem = FitGumbel()

res = minimize(problem,
			   algorithm,
			   verbose=False,
			   seed=1)

mu, beta, norm, center = res.X
rmse_final = res.F

print("%10.4g  mu" % mu.item())
print("%10.4g  beta" % beta.item())
print("%10.4g  norm" % norm.item())
print("%10.4g  center" % center.item())
print("%10.4g  rmse_initial" % rmse_initial)
print("%10.4g  rmse_final" % rmse_final.item())

ftsv = None
if not Args.output is None:
	ftsv = open(Args.output, "w")

nhats = []
nhatsz = []
for binidx in range(nrbins):
	score = scores[binidx]
	n = ns[binidx]
	y = Gumbel(mu, beta, score - center)
	nhat = norm*y
	nhats.append(nhat)
	if n > 0:
		nhatsz.append(nhat)
	if not ftsv is None:
		dn = nhat - n
		s = "%.4g" % score
		s += "\t%d" % n
		s += "\t%.1f" % nhat
		s += "\t%.3g" % dn
		ftsv.write(s + '\n')

if not ftsv is None:
	ftsv.close()

maxn = max(ns)

fig, axs = plt.subplots(1, 2)

for axidx in [0, 1]:
	ax = axs[axidx]
	ax.set_xlabel(Args.xlabel)
	ax.set_ylabel("Nr. hits")

	if axidx == 0:
		w = Args.barwlin
	else:
		w = Args.barwlog

	ax.bar(scoresz, nsz, width=w, label = "Measured", color = "powderblue")
	ax.plot(scoresz, nhatsz, label = "EVD fit", color = "black")

	min_plotted_x = min(scoresz)
	max_plotted_x = max(scoresz)

	ax.legend()
	if axidx == 0:
		if not xlim_lin is None:
			ax.set_xlim(xlim_lin)
			min_plotted_x, max_plotted_x = xlim_lin

		if not ylim_lin is None:
			ax.set_ylim(ylim_lin)
		ax.get_yaxis().set_major_formatter(
			matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
	else:
		ax.set_yscale('log')
		if not xlim_log is None:
			ax.set_xlim(xlim_log)
		if not ylim_log is None:
			ax.set_ylim(ylim_log)

	if axidx == 0 and Args.show_textbox:
		#################################################################
		# Text showing fitted parameters
		textbox_x = max_plotted_x - (max_plotted_x - min_plotted_x)/10
		textbox_y = maxn/3
		if not Args.textbox_x is None:
			textbox_x = Args.textbox_x
		if not Args.textbox_y is None:
			textbox_y = Args.textbox_y
		formula = "\u03bc=%.3g\n\u03b2=%.3g\n\u03b3=%.3g" % (mu, beta, -center)
		props = dict(boxstyle='round', 
					facecolor='whitesmoke',
					edgecolor="lightgray",
					alpha=0.8,
					pad=1)
		ax.text(textbox_x, textbox_y, formula,
				horizontalalignment='right',
				verticalalignment='bottom',
				bbox = props)
		#################################################################
	if not Args.title is None:
		if axidx == 0:
			ax.set_title(Args.title)
		else:
			ax.set_title(Args.title + " (log scale)")

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

set_size(Args.plot_w, Args.plot_h)
fig.tight_layout()
if not Args.nofilename:
	fig.suptitle(Args.plot)
if not Args.plot is None:
	fns = Args.plot
	for fn in fns:
		sys.stderr.write(fn + '\n')
		fig.savefig(fn)
