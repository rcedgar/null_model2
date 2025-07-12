#!/usr/bin/python3

import sys
import math
import argparse
import numpy as np

NQ = 11211

AP = argparse.ArgumentParser()
AP.add_argument("--hits", required=False, default="../big_hits/reseek.scop40")
AP.add_argument("--edf_ref", required=False, default="../edf/reseek.scop40")
AP.add_argument("--lookup", required=False, default="../data/scop40.lookup")
AP.add_argument("--ref_dbsize", type=float, required=False, default=11211)
AP.add_argument("--ts", type=float, required=False)
AP.add_argument("--m", required=False, type=float, default=1.48)
AP.add_argument("--c", required=False, type=float, default=-22.4)
AP.add_argument("--field", required=False, type=int, default=5)
AP.add_argument("--verbose", default=False, action='store_true')

Args = AP.parse_args()

dom2scopid = {}
for line in open(Args.lookup):
	flds = line[:-1].split('\t')
	dom2scopid[flds[0]] = flds[1]

fldnr = Args.field - 1
ref_dbsize = Args.ref_dbsize

def read_dist(fn, distname):
	bin_mids = []
	fld_nr = None
	v = []
	for line in open(fn):
		if line.startswith('#'):
			continue
		if fld_nr is None:
			hdr = line[:-1].split('\t')
			assert hdr[0] == "binmids"
			for i in range(len(hdr)):
				if hdr[i] == distname:
					fld_nr = i
					break
			if fld_nr is None:
				assert False, "distname=%s not found in fn=%s" % (distname, fn)
			continue
		if len(line.strip()) == 0:
			continue
		flds = line[:-1].split('\t')
		bin_mid = float(flds[0])
		x = float(flds[fld_nr])

		bin_mids.append(bin_mid)
		v.append(x)

	return bin_mids, np.array(v, dtype=np.float32)

bin_mids_ref, P_F_score_ref = read_dist(Args.edf_ref, "P_F_score")

def get_P_false_fit(score):
	log10P = Args.m*score + Args.c
	if log10P > 1:
		return 1
	P_false_fit = 10**log10P
	return P_false_fit

def get_P_false_measured(score):
	P_false = np.interp(score, bin_mids_ref, P_F_score_ref)
	return P_false

def get_P_false(score):
	P_false = get_P_false_measured(score)
	if P_false > 0.1:
		return P_false
	P_false_fit = get_P_false_fit(score)
	return P_false_fit

if not Args.ts is None:
	print("          TS  %.3g" % Args.ts)
	print("P_f_measured  %.3g" % get_P_false_measured(Args.ts))
	print("     P_f_fit  %.3g" % get_P_false_fit(Args.ts))
	sys.exit(0)

def predict_EPQ(score):
	nrbins_target = len(bin_mids_target)
	totalfp = 0
	for binidx in range(nrbins_target):
		scoret = bin_mids_target[binidx]
		if scoret >= score:
			n = N_score_target[binidx]
			P_false = get_P_false(scoret)
			totalfp += n*P_false
	EPQ = totalfp/NQ
	return EPQ

qs = set()
q2scorevec = {}
q2tvec = {}
q2Evec = {}
sys.stderr.write("Reading hits\n")
n = 0
for line in open(Args.hits):
	n += 1
	if n%10000 == 0:
		sys.stderr.write("%d\r" % n)
	flds = line[:-1].split('\t')
	q = flds[0]
	t = flds[1]
	E = float(flds[2])
	score = float(flds[fldnr])
	if not q in qs:
		q2scorevec[q] = []
		q2tvec[q] = []
		q2Evec[q] = []
		qs.add(q)
	q2scorevec[q].append(score)
	q2tvec[q].append(t)
	q2Evec[q].append(E)
sys.stderr.write("%d hits\n" % n)

def argsort(seq):
    return sorted(range(len(seq)), key=seq.__getitem__)

sys.stderr.write("Sorting\n")
n = 0
for q in qs:
	n += 1
	sys.stderr.write("%d\r" % n)
	scorevec = q2scorevec[q]
	tvec = q2tvec[q]
	Evec = q2Evec[q]
	nrhits = len(scorevec)
	order = argsort(scorevec)
	K = len(order)
	Ps = []
	for k in range(K):
		P_f = get_P_false(scorevec[k])
		Ps.append(P_f)

	for j in range(K):
		k = order[j]
		t = tvec[k]
		E = Evec[k]
		score = scorevec[k]
		qfam = q + "/" + dom2scopid.get(q, "MISSING")
		tfam = t + "/" + dom2scopid.get(t, "MISSING")
		if 0:
			if Args.verbose:
				print()
				print(qfam, tfam, E)
			EPQ = 0
			for j2 in range(j, K):
				k2 = order[j2]
				# P_f = get_P_false(scorevec[k2])
				P_f = Ps[k2]
				EPQ += P_f
				if Args.verbose:
					s = tvec[k2]
					s += " score=%7.3g" % scorevec[k2]
					s += " P_f=%7.3g" % P_f
					s += " E=%7.3g" % Evec[k2]
					s += " EPQ=%7.3g" % EPQ
					print(s)
		else:
			EPQ = get_P_false(score)
		s = qfam
		s += "\t" + tfam
		s += "\t%.3g" % score
		s += "\t%.3g" % E
		s += "\t%.3g" % EPQ
		print(s)

sys.stderr.write("%d queries\n" % n)
