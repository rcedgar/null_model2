#!/usr/bin/python3

import sys
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

AP = argparse.ArgumentParser()
AP.add_argument("--input", required=False, default="/dev/stdin", help="Input (tsv)")
AP.add_argument("--tsv", required=False, default=None, help="Output (tsv)")
AP.add_argument("--plot", required=False, default=None, help="Output (figure)")
AP.add_argument("--bins", required=False, default=100, type=int)
AP.add_argument("--plotw", required=False, default=5, type=float)
AP.add_argument("--ploth", required=False, default=10, type=float)
AP.add_argument("--barw", required=False, default=1, type=float)
AP.add_argument("--score_field", required=False, default=3, type=int, help="Field nr. (default 1)")
AP.add_argument("--evalue_field", required=False, default=4, type=int, help="Field nr. (default 1)")
AP.add_argument("--minx", required=True, type=float, help="Min value")
AP.add_argument("--dx", required=True, type=float, help="Bin width")
Args = AP.parse_args()

score_fld_nr = Args.score_field - 1
evalue_fld_nr = Args.evalue_field - 1
nr_scorebins = Args.bins
minx = Args.minx
dx = Args.dx
maxx = minx + dx*nr_scorebins

MAXE=1e-3

def get_viridis_color(value):
	"""
	Args:
		value: A floating-point number between 0 and 100 (inclusive).

	Returns:
		A tuple of three floats (R, G, B), each in the range 0 to 1,
		representing the viridis color.  Returns (0, 0, 0) if input is out of range.
	"""
	if not 0 <= value <= 100:
		return (0, 0, 0)  # Return black for out-of-range values

	# Use matplotlib's viridis colormap
	colormap = plt.cm.viridis

	# Get the color from the colormap
	color = colormap(value)

	# The colormap returns RGBA (Red, Green, Blue, Alpha).  We only want RGB.
	r, g, b, _ = color  # Discard the alpha channel
	return (r, g, b)

scores = np.linspace(minx, maxx, nr_scorebins)

# colors = [ "linen", "bisque",	"lime",	"dodgerblue",	"royalblue", "red" ]
# Edges =	[	10,		1,			1e-3,	1e-6,			1e-9,		0]

# colors = [ "bisque",		"dodgerblue",	"lime",	"orange",	"red",	"pink",		"black"]
#Edges =	[	1e-3,			1e-4,			1e-5,	1e-6,		1e-7,	1e-8,			0]
Edges = []
for k in range(5, 13):
	Edges.append(10**(-k))
Edges.append(0)

nr_Ebins = len(Edges) - 1

edges = []
edge = minx
for i in range(nr_scorebins+1):
	edges.append(edge)
	edge += dx

count_mx = []*nr_Ebins
for i in range(nr_Ebins):
	count_mx.append([0]*nr_scorebins)

matplotlib.use("Agg")

v = []
ltmaxe = 0
discarded_top = 0
for line in open(Args.input):
	flds = line[:-1].split('\t')
	sscore = flds[score_fld_nr]
	if sscore == "no_score":
		continue
	score = float(sscore)
	sE = flds[evalue_fld_nr]
	if sE == "no_E":
		continue
	E = float(sE)
	if E > MAXE:
		continue
	ltmaxe += 1
	score_binidx = int((score - minx)*nr_scorebins/(maxx - minx))
	if score_binidx < 0:
		continue
	if  score_binidx >= nr_scorebins:
		discarded_top += 1
		continue
	for Ebinidx in range(nr_Ebins):
		if E <= Edges[Ebinidx] and E > Edges[Ebinidx+1]:
			count_mx[Ebinidx][score_binidx] += 1
		if E < Edges[-1]:
			count_mx[nr_Ebins-1][score_binidx] += 1

sys.stderr.write("ltmaxe=%d, discarded_top=%d\n" % (ltmaxe, discarded_top))

def get_label(E):
	# 1.0e-10
	s = "%.2e" % E
	return "<E-" + s[6:] 

fig, ax = plt.subplots()
bottom = np.zeros(nr_scorebins)
for Ebinidx in range(nr_Ebins):
	# color = colors[Ebinidx]
	row = np.array(count_mx[Ebinidx], dtype=int)
	# if sum(row) < 100:
	# 	continue
	fract = Ebinidx/(nr_Ebins - 1)
	color = get_viridis_color(fract)
	ax.bar(scores, row, width=Args.barw, bottom=bottom, color=color, label=get_label(Edges[Ebinidx]))
	bottom += row

ax.set_xlabel("Pre-filter score")
ax.set_ylabel("Nr. hits")

handles, labels = plt.gca().get_legend_handles_labels()
order = range(len(labels))[::-1]
plt.legend([handles[idx] for idx in order],[labels[idx] for idx in order])

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

if not Args.plot is None:
	set_size(Args.plotw, Args.ploth)
	sys.stderr.write(Args.plot + '\n')
	fig.tight_layout()
	plt.savefig(Args.plot)
