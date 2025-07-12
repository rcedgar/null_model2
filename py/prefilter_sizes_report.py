#!/usr/bin/python3

import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Agg')

def get_ns(fn):
	tphits = None
	fphits = None
	sens = None
	for line in open(fn):
		if line.startswith("# "):
			flds = line[2:-1].split(';')
			for fld in flds:
				if fld.startswith("hits="):
					hits = int(fld.split('=')[1])
				if fld.startswith("tphits="):
					tphits = int(fld.split('=')[1])
				if fld.startswith("sens="):
					sens = float(fld.split('=')[1])
	return sens, hits, tphits

print("K\tX\tfsSens\trsSens\tfsPF\trsPF\tfsPrec\trsPrec")
xsteps = []
xlabels = []
xstep = 0

fPFs = []
rPFs = []

fSens = []
rSens = []

fPrec = []
rPrec = []

def go(K, div, X):
	global xstep, xsteps
	assert not K is None
	if div is None and X is None:
		foldseek_sens, foldseek_hits, foldseek_tphits = get_ns("../edf/foldseek_maxseqs%d.scop40.scop40.scop40" % (K))
		reseek_sens, reseek_hits, reseek_tphits = get_ns("../edf/reseek_rsbsize%d_ts.scop40.scop40.scop40" % (K))
	elif not div is None:
		foldseek_sens, foldseek_hits, foldseek_tphits = get_ns("../edf/foldseek_maxseqs%d.scop40.scop40_div%d.scop40_div%d" % (K, div, div))
		reseek_sens, reseek_hits, reseek_tphits = get_ns("../edf/reseek_rsbsize%d_ts.scop40.scop40_div%d.scop40_div%d" % (K, div, div))
	elif not X is None:
		foldseek_sens, foldseek_hits, foldseek_tphits  = get_ns("../edf/foldseek_maxseqs%d.scop40.scop40x%d.scop40" % (K, X))
		reseek_sens, reseek_hits, reseek_tphits = get_ns("../edf/reseek_rsbsize%d_ts.scop40.scop40x%d.scop40" % (K, X))
	else:
		assert False

	s = "%d" % K

	if not div is None:
		xlabel = "1/%d" % div
	elif not X is None:
		xlabel = "%d" % X
	else:
		xlabel = "1"
	s += "\t" + xlabel

	foldseek_PF = (foldseek_hits - foldseek_tphits)/foldseek_hits
	reseek_PF = (reseek_hits - reseek_tphits)/reseek_hits

	foldseek_Prec = foldseek_tphits/foldseek_hits
	reseek_Prec = reseek_tphits/reseek_hits

	s += "\t%.3g" % foldseek_sens
	s += "\t%.3g" % reseek_sens

	s += "\t%.3g" % foldseek_PF
	s += "\t%.3g" % reseek_PF

	s += "\t%.3g" % foldseek_Prec
	s += "\t%.3g" % reseek_Prec
	
	print(s)

	if K == 100:
		xsteps.append(xstep)
		xlabels.append(xlabel)
		xstep += 1

		fPFs.append(foldseek_PF)
		rPFs.append(reseek_PF)

		fSens.append(foldseek_sens)
		rSens.append(reseek_sens)

		fPrec.append(foldseek_Prec)
		rPrec.append(reseek_Prec)

K = 100

for div in [ 2, 4 ][::-1]:
	go(K, div, None)
go(K, None, None)
for X in [ 2, 4, 8 ]:
	go(K, None, X)

fig, axs = plt.subplots(3, 2)

ax = axs[0][0]
ax.bar(xsteps, fPFs, color = "gray")
ax.set_title("Foldseek max-seqs=100")
ax.set_ylabel("P(F)")
ax.set_xlabel("Database size")
ax.set_xticks(xsteps, xlabels)
ax.set_ylim([0, 1])

ax = axs[0][1]
ax.bar(xsteps, rPFs, color = "gray")
ax.set_ylabel("P(F)")
ax.set_xlabel("Database size")
ax.set_ylim([0, 1])
ax.set_xticks(xsteps, xlabels)
ax.set_title("Reseek rsb_size=100")

ax = axs[1][0]
ax.bar(xsteps, fSens, color = "gray")
ax.set_title("Foldseek max-seqs=100")
ax.set_ylabel("Sensitivity")
ax.set_xlabel("Database size")
ax.set_xticks(xsteps, xlabels)
ax.set_ylim([0, 0.7])

ax = axs[1][1]
ax.bar(xsteps, rSens, color = "gray")
ax.set_ylabel("Sensitivity")
ax.set_xlabel("Database size")
ax.set_ylim([0, 0.7])
ax.set_xticks(xsteps, xlabels)
ax.set_title("Reseek rsb_size=100")

ax = axs[2][0]
ax.bar(xsteps, fPrec, color = "gray")
ax.set_title("Foldseek max-seqs=100")
ax.set_ylabel("Precision")
ax.set_xlabel("Database size")
ax.set_xticks(xsteps, xlabels)
ax.set_ylim([0, 1])

ax = axs[2][1]
ax.bar(xsteps, rPrec, color = "gray")
ax.set_ylabel("Precision")
ax.set_xlabel("Database size")
ax.set_ylim([0, 1])
ax.set_xticks(xsteps, xlabels)
ax.set_title("Reseek rsb_size=100")

fig.set_size_inches(8, 6)
fig.tight_layout()
fn = "prefilter_histogram.svg"
sys.stderr.write(fn + '\n')
fig.savefig(fn)

fn = "prefilter_histogram.png"
sys.stderr.write(fn + '\n')
fig.savefig(fn)
