#!/usr/bin/python3

import sys
import math
import argparse
import numpy as np

NQ = 11211

AP = argparse.ArgumentParser()
AP.add_argument("--edf_ref", required=True)
AP.add_argument("--edf_target", required=True)
AP.add_argument("--ref_dbsize", type=float, required=True)
AP.add_argument("--lo", type=float, required=False)
AP.add_argument("--hi", type=float, required=False)
AP.add_argument("--verbose", type=float, required=False)
AP.add_argument("--scorefmt", required=False, default="%.3g")
AP.add_argument("--m", required=True, type=float)
AP.add_argument("--c", required=True, type=float)

# Just a reminder that E-values are assumed
AP.add_argument("--not_evalue", default=False, action='store_true')

Args = AP.parse_args()

# Just a reminder that E-values are assumed
assert not Args.not_evalue

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

bin_mids_ref, P_T_score_ref = read_dist(Args.edf_ref, "P_T_score")
_, P_F_score_ref = read_dist(Args.edf_ref, "P_F_score")
bin_mids_target, N_score_target = read_dist(Args.edf_target, "N_score")

def get_P_false_fit(score):
	log10P = Args.m*score + Args.c
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

if not Args.verbose is None:
	nrbins_target = len(bin_mids_target)
	score = -math.log10(Args.verbose)
	totalfp = 0
	s = "scoret"
	s += "\tn"
	s += "\tP_false"
	s += "\ttotalfp"
	print(s)
	for binidx in range(nrbins_target):
		scoret = bin_mids_target[binidx]
		if scoret >= score:
			n = N_score_target[binidx]
			P_false = get_P_false(scoret)
			P_false_fit = get_P_false_fit(scoret)
			if P_false > 0.1:
				totalfp += n*P_false
			else:
				totalfp += n*P_false_fit
			s = "%.3g" % scoret
			s += "\t%d" % n
			s += "\t%.4g" % P_false
			s += "\t%.4g" % P_false_fit
			s += "\t%.3g" % totalfp
			print(s)
	EPQ = totalfp/NQ
	sys.exit(0)

def fmte(E):
	if E > 10:
		return ">10"
	elif E < 1e-3:
		return "%.2e" % E
	else:
		return "%.3g" % E

s = "Evalue"
s += "\tE"
s += "\tP(F|score)"
s += "\tP(T|score)"
print(s)

E = Args.lo
while True:
	score = -math.log10(E)
	Pf = get_P_false(score)
	Pt = 1 - Pf
	EPQ_target = predict_EPQ(score)

	s = fmte(E)
	s += "\t" + fmte(EPQ_target)
	s += "\t%.3g" % Pf
	s += "\t%.3f" % Pt
	print(s)
	E *= 10
	# hack to fix rounding error
	if E > 9 and E < 11:
		E = 10
	if E > Args.hi:
		break

print('# ' + ' '.join(sys.argv))