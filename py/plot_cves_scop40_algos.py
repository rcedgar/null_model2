#!/usr/bin/python3

import sys
import os
from plot_dists_lib import *
import matplotlib
import matplotlib.pyplot as plt

scop = sys.argv[1]

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

matplotlib.use('Agg')

xlim40 = None
ylim = [0.01, 10]

colors = [ "firebrick", "lightcoral", "gold"  ]
fig, axs = plt.subplots(1, 2)

############################
# CVEs
############################
_, cve_sens_reseek = read_dist("../edf/reseek_sensitive_ts.scop40.scop40." + scop, "cve_sens")
_, cve_epq_reseek = read_dist("../edf/reseek_sensitive_ts.scop40.scop40." + scop, "cve_epq")

_, cve_sens_foldseek = read_dist("../edf/foldseek_default.scop40.scop40." + scop, "cve_sens")
_, cve_epq_foldseek = read_dist("../edf/foldseek_default.scop40.scop40." + scop, "cve_epq")

_, cve_sens_tm = read_dist("../edf/tm.scop40.scop40." + scop, "cve_sens")
_, cve_epq_tm = read_dist("../edf/tm.scop40.scop40." + scop, "cve_epq")

_, cve_sens_dali = read_dist("../edf/dali.scop40.scop40." + scop, "cve_sens")
_, cve_epq_dali = read_dist("../edf/dali.scop40.scop40." + scop, "cve_epq")

############################
# CatEs
############################
_, cate_sens_reseek = read_dist("../edf/reseek_sensitive_ts.scop40.scop40." + scop, "cate_sens")
_, cate_epq_reseek = read_dist("../edf/reseek_sensitive_ts.scop40.scop40." + scop, "cate_epq")

_, cate_sens_foldseek = read_dist("../edf/foldseek_default.scop40.scop40." + scop, "cate_sens")
_, cate_epq_foldseek = read_dist("../edf/foldseek_default.scop40.scop40." + scop, "cate_epq")

_, cate_sens_tm = read_dist("../edf/tm.scop40.scop40." + scop, "cate_sens")
_, cate_epq_tm = read_dist("../edf/tm.scop40.scop40." + scop, "cate_epq")

_, cate_sens_dali = read_dist("../edf/dali.scop40.scop40." + scop, "cate_sens")
_, cate_epq_dali = read_dist("../edf/dali.scop40.scop40." + scop, "cate_epq")

ax = axs[0]
ax.plot(cve_sens_dali, cve_epq_dali, label="DALI", color = "green")
ax.plot(cve_sens_foldseek, cve_epq_foldseek, label="Foldseek", color = "orange")
ax.plot(cve_sens_tm, cve_epq_tm, label="TM-align", color = "firebrick")
ax.plot(cve_sens_reseek, cve_epq_reseek, label="Reseek", color = "black")

ax.set_xlabel("Sensitivity")
ax.set_ylabel("FPEPQ")
ax.set_yscale('log')
ax.set_xlim([0, 0.6])
ax.set_ylim([0.01, 10])
ax.legend()

ax = axs[1]
ax.plot(cate_sens_dali, cate_epq_dali, label="DALI", color = "green")
ax.plot(cate_sens_foldseek, cate_epq_foldseek, label="Foldseek", color = "orange")
ax.plot(cate_sens_tm, cate_epq_tm, label="TM-align", color = "firebrick")
ax.plot(cate_sens_reseek, cate_epq_reseek, label="Reseek", color = "black")

ax.set_xlabel("Category coverage")
ax.set_ylabel("FPEPQ")
ax.set_yscale('log')
ax.set_xlim([0.4, 1.0])
ax.set_ylim([0.0001, 0.1])
ax.legend()
set_size(6, 2.25)
fig.tight_layout()

os.system("mkdir -p ../cves")
svg_fn = "../cves/cves_" + scop + "_algos.svg"
sys.stderr.write(svg_fn + '\n')
fig.savefig(svg_fn)

png_fn = "../cves/cves_" + scop + "_algos.png"
sys.stderr.write(png_fn + '\n')
fig.savefig(png_fn)
