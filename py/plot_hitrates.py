#!/usr/bin/python3

import sys
import re
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

ftsv = open("hitrate.tsv", "w")

matplotlib.use('Agg')

def get_edffn(algo, q, db, ref):
	return "../edf/" + algo + "." + q + "." + db + "." + ref

def get_hitrate(edffn):
	hitrate = None
	for line in open(edffn):
		if not line.startswith("#"):
			continue
		if line.find("hitrate=") > 0:
			M = re.search(r"hitrate=([0-9.e]+);", line)
			hitrate = float(M.group(1))
	assert not hitrate is None
	return hitrate

qs =		[ "scop40n4",	"scop40n2",	"scop40",	"scop40",	"scop40",	"scop40",	"scop40",	"scop40" ]
dbs =		[ "scop40n4",	"scop40n2",	"scop40",	"scop40x2", "scop40x4", "scop40x8", "bfvd",		"pdb" ]
xlabels =	[ "/4",			"/2",		"x1",		"x2",		"x4",		"x8",		"BFVD",		"PDB" ]
refdbs =	[ "scop40",		"scop40",	"scop40",	"scop40",	"scop40",	"scop40",	"none",		"none"  ]

nrdbs = len(dbs)
xsteps = range(nrdbs)

reseek_hitrates = []
foldseek_hitrates = []

s = "db"
s += "\treseek"
s += "\tfoldseek"
ftsv.write(s + '\n')

for q, db, ref, xlabel in zip(qs, dbs, refdbs, xlabels):
	reseek_edffn = get_edffn("reseek_sensitive_ts", q, db, ref)
	foldseek_edffn = get_edffn("foldseek_exhaustive", q, db, ref)

	reseek_hitrate = get_hitrate(reseek_edffn)
	foldseek_hitrate = get_hitrate(foldseek_edffn)

	reseek_hitrates.append(reseek_hitrate)
	foldseek_hitrates.append(foldseek_hitrate)

	s = xlabel
	s += "\t%.3g" % reseek_hitrate
	s += "\t%.3g" % foldseek_hitrate
	ftsv.write(s + '\n')
ftsv.close()

fig, axs = plt.subplots(2, 1)

ax = axs[0]
ax.bar(xsteps, foldseek_hitrates, color = "gray")
# ax.set_title("Foldseek")
ax.set_ylabel("Foldseek h")
ax.set_xticks(xsteps, xlabels)

ax = axs[1]
ax.bar(xsteps, reseek_hitrates, color = "gray")
# ax.set_title("Reseek")
ax.set_ylabel("Reseek h (TS)")
ax.set_xlabel("Database")
ax.set_xticks(xsteps, xlabels)

fig.set_size_inches(6, 4)
fig.tight_layout()
fn = "hitrate.svg"
sys.stderr.write(fn + '\n')
fig.savefig(fn)

fn = "hitrate.png"
sys.stderr.write(fn + '\n')
fig.savefig(fn)
