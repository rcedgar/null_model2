#!/usr/bin/python3

import sys
import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

matplotlib.use('Agg')

rtsv = "../prefilter_top_hits/reseek_scop40_afdb50.tsv"
ftsv = "../prefilter_top_hits/foldseek_scop40_afdb50.tsv"

def readfn(fn):
	Ps = []
	rank = 0
	for line in open(fn):
		flds = line[:-1].split('\t')
		assert len(flds) == 3
		assert int(flds[0]) == rank
		Ps.append(100*(1 - float(flds[2])/float(flds[1])))
		rank += 1
	return Ps

rPs = readfn(rtsv)
fPs = readfn(ftsv)

N = len(rPs)
assert len(fPs) == N
ranks = range(1, N+1)

def get_viridis_color(value):
	assert 0 <= value <= 1
	colormap = plt.cm.viridis
	color = colormap(float(value))
	r, g, b, _ = color  # Discard the alpha channel
	return (r, g, b)

fig, ax = plt.subplots(1, 1)

ax.set_title("Fraction of top hits discarded by prefilter")
ax.set_ylabel("Pct.")
ax.set_xlabel("Rank")
ax.set_ylim(0.0, 20)

n = 10
xsteps = []
xlabels = []
for i in range(1, n+1):
	xsteps.append(i)
	xlabels.append("%d" % (i))
ax.set_xticks(xsteps, xlabels)

ax.plot(ranks[0:n], fPs[0:n], label="Foldseek", marker="o", linewidth=0)
ax.plot(ranks[0:n], rPs[0:n], label="Reseek", marker="o", linewidth=0)
ax.legend()

fig.set_size_inches(4, 2.5)
fig.tight_layout()

sys.stderr.write("../prefilter_top_hits/fig.svg\n")
fig.savefig("../prefilter_top_hits/fig.svg")

sys.stderr.write("../prefilter_top_hits/fig.png\n")
fig.savefig("../summary_pngs/prefilter_top_hits.png")
