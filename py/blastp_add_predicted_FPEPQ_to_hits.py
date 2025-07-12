#!/usr/bin/python3

import re
import sys
import math
import argparse

AP = argparse.ArgumentParser()
AP.add_argument('--hits', default="../big_hits/blastp.scop40")
AP.add_argument('--prior_pf', type=float, default=0.5)
AP.add_argument('--m', type=float, default=0.09978)
AP.add_argument('--c', type=float, default=-4.944)
AP.add_argument('--nh', type=int, default=145114)
AP.add_argument('--nq', type=int, default=11211)
Args = AP.parse_args()

hitsfn = Args.hits
prior_pf = Args.prior_pf
m = Args.m
c = Args.c
NH_target = Args.nh
NQ_target = Args.nq

def estimate_C(score, m, c):
	logC = -(m*score + c)
	C = min(10**logC, 1)
	return C

def estimate_FPEPQ(score, m, c, NH_target, NQ_target):
	C = estimate_C(score, m, c)
	FPEPQ = prior_pf*C*NH_target/NQ_target
	return FPEPQ

for line in open(hitsfn):
	line = line[:-1]
	flds = line.split('\t')
	score = float(flds[3])
	FPEPQ = estimate_FPEPQ(score, m, c, NH_target, NQ_target)
	line += "\t%.3g" % FPEPQ
	print(line)
