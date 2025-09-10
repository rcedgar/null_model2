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
from matplotlib.transforms import Bbox
from matplotlib.lines import Line2D
import matplotlib.gridspec as gridspec
from plot_dists_lib import read_dist

matplotlib.use('Agg')

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

# value 0..1
def get_viridis_color(value):
	colormap = plt.cm.viridis
	color = colormap(value)
	r, g, b, _ = color  # Discard the alpha channel
	return (r, g, b)

#####################################################
# Grid layout
#####################################################
the_labels = [ \
		"CATH40", \
		"SCOP40x8", \
		"SCOP40x4", \
		"SCOP40x2", \
		"SCOP40", \
		"SCOP95", \
		"SCOP40/2", \
		"SCOP40/4", \
		"SCOP40/SF2", \
		"SCOP40/SF4", \
		"Ideal E-value" ]

label2color = { \
		"SCOP40x8" : get_viridis_color(0), \
		"SCOP40x4" : get_viridis_color(0.2), \
		"SCOP40x2" : get_viridis_color(0.4), \
		"SCOP40" : get_viridis_color(0.6), \
		"SCOP95" : "cyan", \
		"CATH40" : "orange", \
		"SCOP40/2" : get_viridis_color(0.8), \
		"SCOP40/4" : get_viridis_color(0.99), \
		"SCOP40/SF2" : get_viridis_color(0.67), \
		"SCOP40/SF4" : get_viridis_color(0.83), \
		"Ideal E-value" : "black" }

label2linestyle = { \
		"SCOP40x8" : "solid", \
		"SCOP40x4" : "solid", \
		"SCOP40x2" : "solid", \
		"SCOP40" : "solid", \
		"SCOP95" : "solid", \
		"CATH40" : "solid", \
		"SCOP40/2" : "solid", \
		"SCOP40/4" : "solid", \
		"SCOP40/SF2" : "dashed", \
		"SCOP40/SF4" : "dotted",
		"Ideal E-value" : "dashed" }

#####################################################
# Grid layout
#####################################################
plot_w = 8
plot_h = 4

fig, all_axs = plt.subplots(2, 3)

# fig = plt.figure(figsize=(plot_w, plot_h))
# gs = gridspec.GridSpec(3, 3, figure=fig, height_ratios=[1, 1, 0.2])

# all_axs = []
# all_axs.append([None, None, None])
# all_axs.append([None, None, None])
# all_axs.append([None])
# for i in range(2):
#     for j in range(3):
#         all_axs[i][j] = fig.add_subplot(gs[i, j])

#####################################################
# Foldseek Gumbel fit
#####################################################
output = None
foldseek_outlier = False
foldseek_init = False
hack = False
title = None
plot_fn = "../tmp/combo_fig.svg"
hist = "../fit_gumbel/foldseek_diffscore.hist"
xlim_lin = [ -25, 60 ]
xlim_log = [ -50, 100 ]
ylim_lin = None
ylim_log = [ 1e4, 4e7 ]
minscore = -25
maxscore = 100
xlabel = "Foldseek raw score"
nofilename = True

scores = []
scoresz = []
ns = []
nsz = []
modal_score = None
maxcount = 0
K = 0
for line in open(hist):
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
	if n > 0:
		scoresz.append(score)
		nsz.append(n)
mean_score = K/sum(ns)

nrbins = len(ns)
dx = scores[1] - scores[0]
# assert scores increasing at constant intervals
for binidx in range(1, nrbins):
	thisdx = scores[binidx] - scores[binidx-1]
	assert thisdx > 0
	assert thisdx/dx > 0.99 and thisdx/dx < 1.01, \
		"[%d] %.3g %.3g dx=%.3g thisdx=%.3g" % (binidx, scores[binidx-1], scores[binidx], dx, thisdx)

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

warning_done = False
def rmse(mu, beta, norm, center):
	global warning_done
	d = 0
	for binidx in range(nrbins):
		score = scores[binidx]
		if not minscore is None and score < minscore:
			continue
		if not maxscore is None and score > maxscore:
			continue
		n = ns[binidx]
		if n == 0:
			continue
		y = Gumbel(mu, beta, score - center)
		nhat = norm*y
		dn = nhat - n
		if 0:
			if not warning_done:
				sys.stderr.write("\n***********\nWARNING FIXME\n**************\n")
				warning_done = True
			d += abs(dn)
		else:
			d += dn**2
	return math.sqrt(d)

algorithm = PatternSearch()
scorerange = maxscore - minscore

# mu, beta, norm, center
if foldseek_init:
	xls = [	-2,	initial_beta/10,	initial_norm/10,	-2 ]
	xus = [	2,	initial_beta*10,	initial_norm*10,	2	]
elif hack:
	xls = [	0,	10,	initial_norm/10,	-500 ]
	xus = [	1000,	50,	initial_norm*10,	500	]
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

nhats = []
nhatsz = []
nhatsz = []
residuals = []
accum_residuals = []
sumres = 0
for binidx in range(nrbins):
	score = scores[binidx]
	n = ns[binidx]
	if n == 0:
		continue
	
	nhat = norm*Gumbel(mu, beta, score - center)
	nhats.append(nhat)
	nhatsz.append(nhat)
	residual = n - nhat
	sumres += residual
	residuals.append(residual)
	accum_residuals.append(sumres)

maxn = max(ns)

axs = [ all_axs[0][0], all_axs[0][1] ]
for axidx in [0, 1]:
	ax = axs[axidx]
	ax.set_xlabel(xlabel)
	ax.set_ylabel("Nr. hits")

	barwlin = 1.7
	barwlog = 1.7
	if axidx == 0:
		w = barwlin
	else:
		w = barwlog

	if axidx == 0:
		ax.bar(scoresz, nsz, width=w, label = "Measured", color = "lightgray")
		ax.plot(scoresz, nhatsz, label = "EVD fit", color = "black")
	else:
		ax.bar(scoresz, nhatsz, width=w, label = "Fitted", color = get_viridis_color(0.4))
		ax.bar(scoresz, residuals, bottom=nhatsz, width=w, label = "Excess", color = get_viridis_color(0.9))
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
			# matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
			matplotlib.ticker.FuncFormatter(lambda x, pos: f'{x*1e-6:.1f}M'))
	else:
		ax.set_yscale('log')
		if not xlim_log is None:
			ax.set_xlim(xlim_log)
		if not ylim_log is None:
			ax.set_ylim(ylim_log)
	if not title is None:
		ax.set_title(title)

############################################################
# E-value vs. FPEPQ scaling
############################################################
ideal_color = label2color["Ideal E-value"]
ideal_linestyle = label2linestyle["Ideal E-value"]

############################################################
# Foldseek E-value vs. FPEPQ scaling
############################################################
ax = all_axs[1][0]
ax.set_xlabel("Foldseek E-value")
ax.set_ylabel("Measured FPEPQ")

edffns = [ \
		"../edf/foldseek_default.scop40.scop40x8.scop40", \
		"../edf/foldseek_default.scop40.scop40x4.scop40", \
		"../edf/foldseek_default.scop40.scop40x2.scop40", \
		"../edf/foldseek_default.scop40.scop40.scop40", \
		"../edf/foldseek_default.scop40.scop40_div2.scop40_div2", \
		"../edf/foldseek_default.scop40.scop40_div4.scop40_div4" ]

labels = [ \
		"SCOP40x8", \
		"SCOP40x4", \
		"SCOP40x2", \
		"SCOP40", \
		"SCOP40/2", \
		"SCOP40/4" ]

N = len(edffns)
assert len(labels) == N
minscore = -1
maxscore = 10
for idx in range(N):
	epqs = []
	evalues = []
	ideals = []
	scores, cve_epqs = read_dist(edffns[idx], "cve_epq")
	for score in range(minscore, maxscore+1):
		epq = np.interp(score, scores, cve_epqs)
		evalue = 10**(-score)
		epqs.append(epq)
		evalues.append(evalue)
		ideals.append(evalue)
		label = labels[idx]
		color = label2color[label]
		linestyle = label2linestyle[label]
	ax.plot(evalues, epqs, color=color, linestyle=linestyle)

ax.plot(ideals, ideals, label="Ideal E-value", \
	color=ideal_color, linestyle=ideal_linestyle)

# ax.legend()

ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlim([1e-10, 10])
ax.set_ylim([1e-3,1000])

############################################################
# Reseek E-value vs. FPEPQ scaling
############################################################
ax = all_axs[1][1]
ax.set_xlabel("Reseek E-value")
ax.set_ylabel("Measured FPEPQ")

edffns = [ \
		"../edf/reseek_sensitive_evalue.scop40.scop40x8.scop40", \
		"../edf/reseek_sensitive_evalue.scop40.scop40x4.scop40", \
		"../edf/reseek_sensitive_evalue.scop40.scop40x2.scop40", \
		"../edf/reseek_sensitive_evalue.scop40.scop40.scop40", \
		"../edf/reseek_sensitive_evalue.scop40.scop40_div2.scop40_div2", \
		"../edf/reseek_sensitive_evalue.scop40.scop40_div4.scop40_div4" ]

labels = [ \
		"SCOP40x8", \
		"SCOP40x4", \
		"SCOP40x2", \
		"SCOP40", \
		"SCOP40/2", \
		"SCOP40/4" ]

N = len(edffns)
assert len(labels) == N
minscore = -1
maxscore = 10
for idx in range(N):
	epqs = []
	evalues = []
	ideals = []
	scores, cve_epqs = read_dist(edffns[idx], "cve_epq")
	for score in range(minscore, maxscore+1):
		epq = np.interp(score, scores, cve_epqs)
		evalue = 10**(-score)
		epqs.append(epq)
		evalues.append(evalue)
		ideals.append(evalue)
		label = labels[idx]
		color = label2color[label]
		linestyle = label2linestyle[label]
	ax.plot(evalues, epqs, label=label, color=color, linestyle=linestyle)

ax.plot(ideals, ideals, label="Ideal E-value", \
	color=ideal_color, linestyle=ideal_linestyle)

# ax.legend()

ax.set_xscale('log')
ax.set_yscale('log')
# ax.set_xlim([1e-3, 10])
# ax.set_ylim([1e-2, 10])
ax.set_xlim([1e-10, 10])
ax.set_ylim([1e-3,1000])

############################################################
# P(F|TS) Reseek
############################################################
ax = all_axs[0][2]
scores, P_F_score = read_dist("../edf/reseek_sensitive_ts.scop40.scop40.scop40", "P_F_score")
scores, P_F_score2 = read_dist("../edf/reseek_sensitive_ts.scop40sf2.scop40sf2.scop40", "P_F_score")
scores, P_F_score4 = read_dist("../edf/reseek_sensitive_ts.scop40sf4.scop40sf4.scop40", "P_F_score")

label = "SCOP40"
ax.plot(scores, P_F_score, label=label, color=label2color[label], linestyle=label2linestyle[label])

label = "SCOP40/SF2"
ax.plot(scores, P_F_score2, label=label, color=label2color[label], linestyle=label2linestyle[label])

label = "SCOP40/SF4"
ax.plot(scores, P_F_score4, label=label, color=label2color[label], linestyle=label2linestyle[label])

ax.set_xlim([0.08, 0.18])
ax.set_ylim([0, 0.8])
ax.set_xlabel("Reseek TS")
ax.set_ylabel("P(F|TS)")
ax.legend()

############################################################
# P(TS|F) universal Reseek
############################################################
ax = all_axs[1][2]
scores, P_F_score = read_dist("../edf/reseek_sensitive_ts.scop40.scop40.scop40", "P_score_F")
scores, P_F_score_cath40 = read_dist("../edf/reseek_sensitive_ts.cath40.cath40.cath40", "P_score_F")
scores, P_F_score_n2 = read_dist("../edf/reseek_sensitive_ts.scop40n2.scop40n2.scop40", "P_score_F")
scores, P_F_score_n4 = read_dist("../edf/reseek_sensitive_ts.scop40n4.scop40n4.scop40", "P_score_F")
scores, P_F_score_sf2 = read_dist("../edf/reseek_sensitive_ts.scop40sf2.scop40sf2.scop40", "P_score_F")
scores, P_F_score_sf4 = read_dist("../edf/reseek_sensitive_ts.scop40sf4.scop40sf4.scop40", "P_score_F")
scores, P_F_score_scop95 = read_dist("../edf/reseek_sensitive_ts.scop95.scop95.scop95", "P_score_F")
scores, P_F_score_x8 = read_dist("../edf/reseek_sensitive_ts.scop40.scop40x8.scop40", "P_score_F")

label = "SCOP40x8"
ax.plot(scores, P_F_score_x8, label=label, color=label2color[label], linestyle=label2linestyle[label])

label = "CATH40"
ax.plot(scores, P_F_score_cath40, label=label, color=label2color[label], linestyle=label2linestyle[label])

label = "SCOP95"
ax.plot(scores, P_F_score_scop95, label=label, color=label2color[label], linestyle=label2linestyle[label])

label = "SCOP40"
ax.plot(scores, P_F_score, label=label, color=label2color[label], linestyle=label2linestyle[label])

label = "SCOP40/SF2"
ax.plot(scores, P_F_score_sf2, label=label, color=label2color[label], linestyle=label2linestyle[label])

label = "SCOP40/SF4"
ax.plot(scores, P_F_score_sf4, label=label, color=label2color[label], linestyle=label2linestyle[label])

label = "SCOP40/2"
ax.plot(scores, P_F_score_n2, label=label, color=label2color[label], linestyle=label2linestyle[label])

label = "SCOP40/4"
ax.plot(scores, P_F_score_n4, label=label, color=label2color[label], linestyle=label2linestyle[label])
ax.set_xlim([0.05, 0.15])
ax.set_ylim([1e-3, 1])
ax.set_xlabel("Reseek TS")
ax.set_ylabel("P(TS|F)")
ax.set_yscale('log')
# ax.legend()

# linestyles = []
# colors = []
# for label in the_labels:
# 	colors.append(label2color[label])
# 	linestyles.append(label2linestyle[label])

# # Extra axis spanning bottom row for legend
# legend_ax = fig.add_subplot(gs[2, :])
# legend_ax.axis("off")  # hide ticks & frame

# # Dummy handles for legend
# handles = [Line2D([0], [0], color=c, linestyle=ls) 
#            for c, ls in zip(colors, linestyles)]

# legend_ax.legend(handles, the_labels,
#                  loc="center",
#                  ncol=6,
#                  frameon=False)

############################################################
# Final figure
############################################################
set_size(plot_w, plot_h)
fig.tight_layout()
sys.stderr.write(plot_fn + '\n')
fig.savefig(plot_fn)
