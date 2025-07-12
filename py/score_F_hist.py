#!/usr/bin/python3

# See also score_F_hist_v2.py uses --minscore --delta instead 
#   of --minscore --maxscore to mitigate
#	effects of binning integer scores

import sys
import argparse
import math
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from empdist import EmpiricalDistributions

matplotlib.use('Agg')

AP = argparse.ArgumentParser()
AP.add_argument("--hits", required=True, help="Hits tsv")
AP.add_argument("--lookup", required=False, type=str, default="../data/scop40.lookup", 
				help="Tsv with 1. domain 2. scopid e.g. a.1.2.3, default ../data/scop40.lookup")
AP.add_argument("--fields", required=False, default="1,2,3", help="query,target,score field numbers (default 1,2,3)")
AP.add_argument("--minscore", required=True, type=float, help="Min score for binning (delete if lower)")
AP.add_argument("--maxscore", required=True, type=float, help="Max score for binning (delete if higher)")
AP.add_argument("--bins", required=False, type=int, default=32, help="Nr. bins")
AP.add_argument("--output", required=False, type=str, help="Output TSV")
AP.add_argument("--evalues", required=False, default=False, action="store_true", help="E-values, use score = -log10(score_field)")
AP.add_argument("--foldseek_outlier", required=False, default=False, action="store_true", help="Correct for Foldseek anomaly at bits=0")
Args = AP.parse_args()

nrbins = Args.bins

fs = Args.fields.split(",")
if len(fs) != 3:
		assert False, "--fields must be 3 comma-separated 1-based field numbers"

qfldnr = int(fs[0]) - 1
tfldnr = int(fs[1]) - 1
scorefldnr = int(fs[2]) - 1

ED = EmpiricalDistributions(nrbins, "/dev/null")
ED.filtered_hits = None
ED.evalues = Args.evalues
ED.minscore = Args.minscore
ED.maxscore = Args.maxscore
ED.minevalue = 1e-20
ED.maxevalue = 1000
ED.read_lookup(Args.lookup)
ED.read_hits(Args.hits, qfldnr, tfldnr, scorefldnr)

bin_edges = np.linspace(Args.minscore, Args.maxscore, Args.bins + 1)

scores_F = np.array(ED.scores_F, dtype=np.float32)
h, bin_edges_ = np.histogram(scores_F, bin_edges)

if not Args.output is None:
	with open(Args.output, "w") as ftsv:
		for bin_idx in range(nrbins):
			assert bin_edges_[bin_idx] == bin_edges[bin_idx]
			n = h[bin_idx]
			if Args.foldseek_outlier and bin_edges[bin_idx] == 0:
				n = 0
			s = "%.5g" % bin_edges[bin_idx]
			s += "\t%d" % n
			ftsv.write(s + '\n')