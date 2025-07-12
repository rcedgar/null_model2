#!/usr/bin/python3

import sys
import os
from plot_dists_lib import *
import matplotlib
import matplotlib.pyplot as plt

scop = "scop40"

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

fig, ax = plt.subplots(1, 1)

_, cve_sens_blastpe = read_dist("../edf/blastpe." + scop, "cve_sens")
_, cve_sens_blastpx = read_dist("../edf/blastpx." + scop, "cve_sens")

_, cve_epq_blastpe = read_dist("../edf/blastpe." + scop, "cve_epq")
_, cve_epq_blastpx = read_dist("../edf/blastpx." + scop, "cve_epq")

ax.set_xlabel("Sensitivity")
ax.set_ylabel("FPEPQ")
ax.set_yscale('log')
ax.set_xlim([0, 0.15])
ax.set_ylim([0.0001, 10])

ax.plot(cve_sens_blastpe, cve_epq_blastpe, label="BLASTP E-value", color = "green", linestyle="dashdot")
ax.plot(cve_sens_blastpx, cve_epq_blastpx, label="Bayes E-value", color = "red", linestyle="dotted")
ax.legend()

set_size(3, 2.25)
fig.tight_layout()

os.system("mkdir -p ../cves")
svg_fn = "../cves/blastp.svg"
sys.stderr.write(svg_fn + '\n')
fig.savefig(svg_fn)
