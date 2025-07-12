#!/usr/bin/python3

import sys
import math
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from plot_dists_lib import read_dist

matplotlib.use('Agg')

AP = argparse.ArgumentParser()
AP.add_argument("--hits", required=True)
AP.add_argument("--lookup", required=False, type=str, default="../data/scop40.lookup", 
				help="Tsv with 1. domain 2. scopid e.g. a.1.2.3, default ../data/scop40.lookup")
AP.add_argument("--fields", required=False, default="1,2,3", help="query,target,score field numbers (default 1,2,3)")
AP.add_argument("--evalues", default=False, action="store_true")
AP.add_argument("--plot", type=str, required=False, help="Plot file, default none")
AP.add_argument("--minscore", type=float, required=True)
AP.add_argument("--title")
AP.add_argument("--xlabel", default="score")
AP.add_argument("--delta", type=float, required=True)
AP.add_argument("--bins", type=int, default=100)
Args = AP.parse_args()

xlim = None
ylim = None

fs = Args.fields.split(",")
if len(fs) != 3:
		assert False, "--fields must be 3 comma-separated 1-based field numbers"

qfldnr = int(fs[0]) - 1
tfldnr = int(fs[1]) - 1
scorefldnr = int(fs[2]) - 1

minscore = Args.minscore
delta = Args.delta
nrbins = Args.bins
maxscore = minscore + (nrbins - 1)*delta

counts = [0]*nrbins
tps_sf = [0]*nrbins
fps_sf = [0]*nrbins
fps_fold = [0]*nrbins
fps_sf = [0]*nrbins

scores = []
for binidx in range(nrbins):
	scores.append(minscore + binidx*delta)

def get_binidx(score):
	if score < minscore or score > maxscore:
		return None
	binidx = int((nrbins - 1)*(score - minscore)/(maxscore - minscore))
	assert binidx >= 0 and binidx < nrbins
	return binidx

def get_fold_sf_from_fam(fam):
	flds = fam.split('.')
	assert len(flds) == 4
	sf = flds[0] + "." + flds[1] + '.' + flds[2]
	fold = flds[0] + "." + flds[1]
	return fold, sf

def read_lookup(fn):
	global dom2sf, dom2fold
	dom2fold = {}
	dom2sf = {}
	for line in open(fn):
		flds = line[:-1].split('\t')
		dom = flds[0]
		dom2fold[dom], dom2sf[dom] = get_fold_sf_from_fam(flds[1])

def get_dom_from_label(label):
	label = label.replace(".pdb", "")
	n = label.find('/')
	if n > 0:
		label = label[:n]
	if label.startswith("DUPE"):
		n = label.find('_')
		label = label[n+1:]
	return label

read_lookup(Args.lookup)

for line in open(Args.hits):
	flds = line[:-1].split('\t')
	q = flds[qfldnr]
	q = get_dom_from_label(flds[qfldnr])
	t = get_dom_from_label(flds[tfldnr])
	sscore = flds[scorefldnr]
	if Args.evalues:
		E = float(sscore)
		if E < 1e-20:
			E = 1e-20
		score = -math.log10(E)
	else:
		score = float(sscore)
	qfold, qsf = dom2fold.get(q), dom2sf.get(q)
	tfold, tsf = dom2fold.get(t), dom2sf.get(t)
	if qfold is None or qsf is None or tfold is None or tsf is None:
		continue
	binidx = get_binidx(score)
	if not binidx is None:
		counts[binidx] += 1
		checksum = 0
		if qsf == tsf:
			tps_sf[binidx] += 1
			checksum += 1
		if qsf != tsf and qfold == tfold:
			fps_sf[binidx] += 1
			checksum += 1
		if qsf != tsf:
			fps_sf[binidx] += 1
		if qfold != tfold:
			assert qsf != tsf
			fps_fold[binidx] += 1
			checksum += 1
		assert checksum == 1

def get_viridis_color(value):
	assert 0 <= value <= 1
	colormap = plt.cm.viridis
	color = colormap(float(value))
	r, g, b, _ = color  # Discard the alpha channel
	return (r, g, b)

fig, ax = plt.subplots(1, 1)

ax.set_xlabel(Args.xlabel)
ax.set_ylabel("Nr. hits")
if not Args.title is None:
	ax.set_title(Args.title)
if not xlim is None:
	ax.set_xlim(xlim)
if not ylim is None:
	ax.set_ylim(ylim)
# ax.set_yscale('log')

tps_sf = np.array(tps_sf, dtype=np.int32)
fps_sf = np.array(fps_sf, dtype=np.int32)
fps_fold = np.array(fps_fold, dtype=np.int32)

width = delta*0.8

ax.bar(scores, tps_sf, width = width, label = "TP (SF)", bottom=fps_fold+fps_sf, color=get_viridis_color(1))
ax.bar(scores, fps_sf, width = width, label = "FP (SF)", bottom=fps_fold, color="lightgray") # color=get_viridis_color(0.5))
ax.bar(scores, fps_fold, width = width, label = "FP (Fold)", color=get_viridis_color(0))
ax.legend()

ax.figure.set_size_inches(4.5, 3)
fig.tight_layout()

if not Args.plot is None:
	sys.stderr.write(Args.plot + '\n')
	fig.savefig(Args.plot)
