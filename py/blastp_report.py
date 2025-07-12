#!/usr/bin/python3

import re
import sys
import math
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from plot_dists_lib import read_dist
from smooth import smooth

matplotlib.use('Agg')

hitsfn = "../big_hits/blastp.scop40"

Args_algo = "blastp"
Args_loscore = 10
Args_delta = 1
Args_nrscores = 100
Args_xlabel = "BLASTP raw score"
Args_output = None
Args_prior_pf = 0.5

NH_target = 11211
NQ_target = 145114

target = "scop40"

m = 0.09978
c = -4.944

xlim = None
ylim = [ 1e-12, 100 ]

table_scores = []
score = Args_loscore
for i in range(Args_nrscores):
	table_scores.append(score)
	score += Args_delta

scores = None
nrbins = None
dist_dict = {}

def get_nq(edf_fn):
	for line in open(edf_fn):
		if not line.startswith('#'):
			continue
		M = re.search(r"qsize=(\d+)", line)
		if not M is None:
			return int(M.group(1))
	return None

fout = None
if not Args_output is None:
	fout = open(Args_output, "w")

def estimate_C(score, m, c):
	logC = -(m*score + c)
	C = min(10**logC, 1)
	return C

def estimate_FPEPQ(score, m, c, NH_target, NQ_target):
	C = estimate_C(score, m, c)
	FPEPQ = Args_prior_pf*C*NH_target/NQ_target
	return FPEPQ

for line in open(hitsfn):
	line = line[:-1]
	flds = line.split('\t')
	score = float(flds[3])
	FPEPQ = estimate_FPEPQ(score, m, c, NH_target, NQ_target)
	line += "\t%.3g" % FPEPQ
	print(line)
