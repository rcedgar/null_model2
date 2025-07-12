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
AP.add_argument("--plot", required=False, help="Plot file")
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
AP.add_argument('--textbox_x', type=float)
AP.add_argument('--textbox_y', type=float, default=1e6)
AP.add_argument("--xlabel", default="Score")
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
ns = []
modal_score = None
maxcount = 0
K = 0
for line in open(Args.hist):
	if line.startswith('#'):
		continue
	flds = line[:-1].split('\t')
	score = float(flds[0])
	n = int(flds[1])
	K += score*n
	if n > maxcount:
		modal_score = score
		maxcount = n
	scores.append(score)
	ns.append(n)
mean_score = K/sum(ns)

nrbins = len(ns)
assert len(scores) == nrbins
dx = scores[1] - scores[0]
# assert scores increasing at constant intervals
for binidx in range(1, nrbins):
	thisdx = scores[binidx] - scores[binidx-1]
	assert thisdx > 0
	assert thisdx/dx > 0.99 and thisdx/dx < 1.01, \
		"[%d] %.3g %.3g dx=%.3g thisdx=%.3g" % (binidx, scores[binidx-1], scores[binidx], dx, thisdx)

cumns = []
cumn = 0
for binidx in range(nrbins-1, -1, -1):
	cumn += ns[binidx]
	cumns.append(cumn)
cumns = cumns[::-1]

# print(cumns)
# sys.exit(1)

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
	sumnhat = 0
	for binidx in range(nrbins -1, -1, -1):
		score = scores[binidx]
		if not Args.minscore is None and score < Args.minscore:
			continue
		if not Args.maxscore is None and score > Args.maxscore:
			continue
		cumn = cumns[binidx]
		y = Gumbel(mu, beta, score - center)
		nhat = norm*y
		sumnhat += nhat
		dn = sumnhat - cumn
		d += dn**2
	err = math.sqrt(d)
	return err

algorithm = PatternSearch()
scorerange = maxscore - minscore

initial_mu = 163
initial_beta = 139
initial_center = -166
initial_norm = 1.4e6
sys.stderr.write("*************\n")
sys.stderr.write("WARNING FIXME\n")
sys.stderr.write("*************\n")

# mu, beta, norm, center
xls = [	initial_mu/10,	initial_beta/10,	initial_norm/10,	-scorerange ]
xus = [	initial_mu*10,	initial_beta*10,	initial_norm*10,	scorerange	]

rmse_initial = rmse(initial_mu, initial_beta, initial_norm, 0)
print("%10.4g  initial mu" % initial_mu)
print("%10.4g  initial beta" % initial_beta)
print("%10.4g  initial norm" % initial_norm)
print("%10.4g  initial center" % 0)

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

cumnhats = []
cumnhat = 0
for binidx in range(nrbins-1,-1,-1):
	score = scores[binidx]
	n = ns[binidx]
	y = Gumbel(mu, beta, score - center)
	nhat = norm*y
	cumnhat += nhat
	cumnhats.append(nhat)
	if not ftsv is None:
		dn = nhat - n
		s = "%.4g" % score
		s += "\t%d" % n
		s += "\t%.1f" % nhat
		s += "\t%.3g" % dn
		ftsv.write(s + '\n')
if not ftsv is None:
	ftsv.close()
cumnhats = cumnhats[::-1]

fig, axs = plt.subplots(1, 2)

for axidx in [0, 1]:
	ax = axs[axidx]
	ax.set_xlabel(Args.xlabel)
	ax.set_ylabel("Nr. hits")

	if axidx == 0:
		w = Args.barwlin
	else:
		w = Args.barwlog

#	print("nsz=", nsz)
#	print("nhatsz=", nsz)

#	ax.bar(scoresz, nsz, label = "Measured", color = "powderblue")
	ax.bar(scores, ns, width=w, label = "Measured", color = "powderblue")
	ax.plot(scores, cumnhats, label = "EVD fit", color = "black")

	min_plotted_x = min(scores)
	max_plotted_x = max(scores)

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

	if axidx == 0:
		#################################################################
		# Text showing fitted parameters
		textbox_x = max_plotted_x - (max_plotted_x - min_plotted_x)/10
		if not Args.textbox_x is None:
			textbox_x = Args.textbox_x
		formula = "\u03bc=%.3g\n\u03b2=%.3g\n\u03b3=%.3g" % (mu, beta, -center)
		props = dict(boxstyle='round', 
					facecolor='whitesmoke',
					edgecolor="lightgray",
					alpha=0.8,
					pad=1)
		ax.text(textbox_x, Args.textbox_y, formula,
				horizontalalignment='right',
				verticalalignment='bottom',
				bbox = props)
		#################################################################

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

if not Args.title is None:
	fig.set_title(Args.title)
set_size(7, 2.5)
fig.tight_layout()
# fig.suptitle(Args.plot)
if not Args.plot is None:
	sys.stderr.write(Args.plot + '\n')
	fig.savefig(Args.plot)
