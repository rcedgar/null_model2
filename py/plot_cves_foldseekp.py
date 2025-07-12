#!/usr/bin/python3

import sys
import os
from plot_dists_lib import *
import matplotlib
import matplotlib.pyplot as plt

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

colors = [ "firebrick", "lightcoral", "gold"  ]
fig, ax = plt.subplots(1, 1)

############################
# CVEs
############################

_, cve_sens_foldseek = read_dist("../edf/foldseek.scop40", "cve_sens")
_, cve_epq_foldseek = read_dist("../edf/foldseek.scop40", "cve_epq")

_, cve_sens_foldseekc = read_dist("../edf/foldseek.scop40c", "cve_sens")
_, cve_epq_foldseekc = read_dist("../edf/foldseek.scop40c", "cve_epq")

_, cve_sens_foldseekp = read_dist("../edf/foldseekp.scop40", "cve_sens")
_, cve_epq_foldseekp = read_dist("../edf/foldseekp.scop40", "cve_epq")

_, cve_sens_foldseekpc = read_dist("../edf/foldseekp.scop40c", "cve_sens")
_, cve_epq_foldseekpc = read_dist("../edf/foldseekp.scop40c", "cve_epq")

############################
# CatEs
############################
_, cate_sens_foldseek = read_dist("../edf/foldseek.scop40", "cate_sens")
_, cate_epq_foldseek = read_dist("../edf/foldseek.scop40", "cate_epq")

_, cate_sens_foldseekc = read_dist("../edf/foldseek.scop40c", "cate_sens")
_, cate_epq_foldseekc = read_dist("../edf/foldseek.scop40c", "cate_epq")

_, cate_sens_foldseekp = read_dist("../edf/foldseekp.scop40", "cate_sens")
_, cate_epq_foldseekp = read_dist("../edf/foldseekp.scop40", "cate_epq")

_, cate_sens_foldseekpc = read_dist("../edf/foldseekp.scop40c", "cate_sens")
_, cate_epq_foldseekpc = read_dist("../edf/foldseekp.scop40c", "cate_epq")

ax.plot(cve_sens_foldseek, cve_epq_foldseek, label="E-value, SCOP40", color = "green")
ax.plot(cve_sens_foldseekc, cve_epq_foldseek, label="E-value, SCOP40c", color = "green", linestyle="dashed")
ax.plot(cve_sens_foldseekp, cve_epq_foldseekp, label="Prob, SCOP40", color = "orange")
ax.plot(cve_sens_foldseekpc, cve_epq_foldseekpc, label="Prob, SCOP40c", color = "orange", linestyle="dashed")

ax.set_xlabel("Sensitivity")
ax.set_ylabel("FPEPQ")
ax.set_yscale('log')
ax.set_xlim([0, 0.8])
ax.set_ylim([0.01, 100])
ax.legend()

set_size(3, 2.25)
fig.tight_layout()

os.system("mkdir -p ../cves")
svg_fn = "../cves/cves_foldseekp.svg"
sys.stderr.write(svg_fn + '\n')
fig.savefig(svg_fn)
