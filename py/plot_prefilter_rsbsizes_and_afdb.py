#!/usr/bin/python3

import sys
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Agg')

rsbsizes = [ 4, 8, 16, 32, 64, 128, 256, 512, 1024 ][::-1]

def get_viridis_color(value):
	if not 0 <= value <= 100:
		return (0, 0, 0)  # Return black for out-of-range values
	colormap = plt.cm.viridis
	color = colormap(value)
	r, g, b, _ = color  # Discard the alpha channel
	return (r, g, b)

def read_fn(fn):
	f = open(fn)
	hdr = f.readline()
#	assert hdr.startswith("score\tN_sensitive")
	scores = []
	Ps = []
	for line in f:
		flds = line[:-1].split('\t')
		assert len(flds) == 4
		score = float(flds[0])
		P = float(flds[3])
		scores.append(score)
		Ps.append(P)
	f.close()
	return scores, Ps

fig, ax = plt.subplots()
n = len(rsbsizes)
for i in range(n):
	size = rsbsizes[i]
	fn = "../P_prefilter/rsbsize%d.tsv" % size
	color = get_viridis_color((n-1-i)/(n-2))
	scores, Ps = read_fn(fn)
	label = "rsbsize=%d" % size
	ax.plot(scores, Ps, color=color, label=label)

fn = "../P_prefilter/afdb50.tsv"
color = get_viridis_color(1)
scores, Ps = read_fn(fn)
label = "AFDB50"
ax.plot(scores, Ps, color=color, label=label, linestyle="dashed")

ax.set_xlabel("TS")
ax.set_ylabel("P(pass)")
ax.legend()

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

fig.tight_layout()
set_size(8, 4)

for ext in [ "svg", "png" ]:
	plotfn = "../P_prefilter/P_pass_rsbsizes." + ext
	sys.stderr.write(plotfn + '\n')
	plt.savefig(plotfn)
