#!/usr/bin/python3

import re
import sys
import math
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Agg')

titles = []
plotidx2cols = []
plotidx2labels = []
plotidx2colors = []
plotidx2linestyles = []

def addplot(title):
	titles.append(title)
	plotidx2cols.append([])
	plotidx2labels.append([])
	plotidx2colors.append([])
	plotidx2linestyles.append([])
	
def add(col, label, color="gray", linestyle="solid"):
	plotidx = len(titles) - 1
	plotidx2cols[plotidx].append(col)
	plotidx2labels[plotidx].append(label)
	plotidx2colors[plotidx].append(color)
	plotidx2linestyles[plotidx].append(linestyle)

fast_color = "orange"
sensitive_color = "blue"
est_linestyle = "solid"
msd_linestyle = "dotted"
c_linestyle = "dashdot"
msd_c_linestyle = "solid"
est_c_linestyle = "solid"

addplot("SCOP40 (11k)")
add("fast.scop40.scop40.est", "fast", fast_color, est_linestyle)
add("sensitive.scop40.scop40.est", "sensitive", sensitive_color, est_linestyle)
add("fast.scop40.scop40c.est", "fast/c", fast_color, c_linestyle)
add("sensitive.scop40.scop40c.est", "sensitive/c", sensitive_color, c_linestyle)

addplot("SCOP40 (11k)")
add("fast.scop40.scop40.est", "fast(estd.)", fast_color, est_linestyle)
add("fast.scop40.scop40.msd", "fast(meas.)", fast_color, msd_linestyle)
add("fast.scop40.scop40c.est", "fast(estd.)/c", fast_color, c_linestyle)
add("fast.scop40.scop40c.msd", "fast(meas.)/c", fast_color, msd_c_linestyle)

addplot("SCOP40 (11k)")
add("sensitive.scop40.scop40.est", "sensitive(estd.)", sensitive_color, est_linestyle)
add("sensitive.scop40.scop40.msd", "sensitive(meas.)", sensitive_color, msd_linestyle)
add("sensitive.scop40.scop40c.est", "sensitive(estd.)/c", sensitive_color, est_c_linestyle)
add("sensitive.scop40.scop40c.msd", "sensitive(meas.)/c", sensitive_color, msd_c_linestyle)

addplot("BFVD (350k)")
add("fast.bfvd.scop40.est", "fast", fast_color, est_linestyle)
add("sensitive.bfvd.scop40.est", "sensitive", sensitive_color, est_linestyle)
add("fast.bfvd.scop40c.est", "fast/c", fast_color, est_c_linestyle)
add("sensitive.bfvd.scop40c.est", "sensitive/c", sensitive_color, est_c_linestyle)

addplot("PDB (1M)")
add("fast.pdb.scop40.est", "fast", fast_color, est_linestyle)
add("sensitive.pdb.scop40.est", "sensitive", sensitive_color, est_linestyle)
add("fast.pdb.scop40c.est", "fast/c", fast_color, est_c_linestyle)
add("sensitive.pdb.scop40c.est", "sensitive/c", sensitive_color, est_c_linestyle)

addplot("AFDB50(52M)")
add("fast.afdb50.scop40.est", "fast", fast_color, est_linestyle)
add("sensitive.afdb50.scop40.est", "sensitive", sensitive_color, est_linestyle)
add("fast.afdb50.scop40c.est", "fast/c", fast_color, est_c_linestyle)
add("sensitive.afdb50.scop40c.est", "sensitive/c", sensitive_color, est_c_linestyle)

addplot("fast (SCOP40 ref)")
add("fast.afdb50.scop40.est", "AFDB40")
add("fast.bfvd.scop40.est", "BFVD")
add("fast.pdb.scop40.est", "PDB")
add("fast.scop40.scop40.est", "SCOP40")

addplot("sensitive (SCOP40 ref)")
add("sensitive.afdb50.scop40.est", "AFDB40")
add("sensitive.bfvd.scop40.est", "BFVD")
add("sensitive.pdb.scop40.est", "PDB")
add("sensitive.scop40.scop40.est", "SCOP40")

addplot("fast (SCOP40c ref)")
add("fast.afdb50.scop40c.est", "AFDB40")
add("fast.bfvd.scop40c.est", "BFVD")
add("fast.pdb.scop40c.est", "PDB")
add("fast.scop40.scop40c.est", "SCOP40")

addplot("sensitive (SCOP40c ref)")
add("sensitive.afdb50.scop40c.est", "AFDB40")
add("sensitive.bfvd.scop40c.est", "BFVD")
add("sensitive.pdb.scop40c.est", "PDB")
add("sensitive.scop40.scop40c.est", "SCOP40")

f = open("../reseek_calibrate3/evalue.tsv")
hdr = f.readline()
cols = hdr[:-1].split('\t')
nrcols = len(cols)

col2idx = {}
for idx in range(nrcols):
	col = cols[idx]
	col2idx[col] = idx
tss = []
rows = []
for line in f:
	flds = line[:-1].split('\t')
	assert len(flds) == nrcols
	ts = float(flds[0])
	tss.append(ts)
	row = []
	for idx in range(nrcols):
		try:
			value = float(flds[idx])
		except:
			value = None
		row.append(value)
	rows.append(row)

nrplots = len(titles)
plots_per_row = 5
assert nrplots%plots_per_row == 0

fig, axs = plt.subplots(nrplots//plots_per_row, plots_per_row)

for plotidx in range(nrplots):
	ax = axs[plotidx//plots_per_row][plotidx%plots_per_row]
	ax.set_title(titles[plotidx])

	ax.set_xlabel("TS")
	ax.set_ylabel("Estimated E-value")

	ax.set_yscale('log')
	ax.set_ylim([1e-9, 10])
	ax.set_xlim([0.2, 0.8])
	cols = plotidx2cols[plotidx]
	labels = plotidx2labels[plotidx]
	colors = plotidx2colors[plotidx]
	linestyles = plotidx2linestyles[plotidx]
	n = len(cols)
	for i in range(n):
		col = cols[i]
		colidx = col2idx[col]
		values = []
		for j in range(len(rows)):
			values.append(rows[j][colidx])
		ax.plot(tss, values, \
			label=labels[i], color=colors[i], linestyle=linestyles[i])
	ax.legend()

ax.figure.set_size_inches(3*plots_per_row, 3*nrplots//plots_per_row)
fig.tight_layout()
for ext in [ "svg", "png" ]:
	fn = "reseek_calibrate3." + ext
	sys.stderr.write(fn + '\n')
	fig.savefig(fn)
