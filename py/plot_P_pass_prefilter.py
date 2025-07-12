#!/usr/bin/python3

import sys
import re
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Agg')

fig, ax = plt.subplots(1, 1)

def dofile(fn, name):
	f = open(fn)
	hdr = f.readline()
	scores = []
	Ps = []
	for line in f:
		flds = line[:-1].split('\t')
		score = float(flds[0])
		if fn.find("afdb") > 0:
			P = float(flds[2])
		else:
			P = float(flds[3])
		scores.append(score)
		Ps.append(P)
	ax.plot(scores, Ps, label=name)

dofile("afdb50.tsv", "AFDB")
dofile("bfvd.tsv", "BFVD")
dofile("pdb.tsv", "PDB")
dofile("scop40.tsv", "SCOP40")

ax.set_xlabel("TS")
ax.set_ylabel("P(pass prefilter|TS)")
ax.legend()

fig.set_size_inches(6, 4)
fig.tight_layout()

fn = "P_pass_prefilter_combined.svg"
sys.stderr.write(fn + '\n')
fig.savefig(fn)

fn = "P_pass_prefilter_combined.png"
sys.stderr.write(fn + '\n')
fig.savefig(fn)
