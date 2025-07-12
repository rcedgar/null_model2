#!/usr/bin/python3

import sys
import math
import argparse
import numpy as np

AP = argparse.ArgumentParser()
AP.add_argument("--edf", required=True)
AP.add_argument("--score", type=float, required=True)
AP.add_argument("--delta", required=True, type=float)
AP.add_argument("--steps", required=True, type=int)
AP.add_argument("--refdbsize", required=True, type=float)
AP.add_argument("--scorefmt", required=False, default="%.3g")
Args = AP.parse_args()

dbnames = []
db2size = {}

def add_db(name, size):
    dbnames.append(name)
    db2size[name] = size

add_db("AFDB", 50e6)
add_db("PDB", 884129)
add_db("BFVD", 347514)
add_db("SCOP40", 11211)

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

bin_mids, P_T_score = read_dist(Args.edf, "P_T_score")
_, EPQ_score = read_dist(Args.edf, "cve_epq")
bin_mids = np.array(bin_mids, dtype=np.float32)

def get_P(score, PDF):
	P = np.interp(score, bin_mids, PDF)
	return P.item()

s = "Evalue\tE\tP(T|SCOP40)"
print(s)

for k in range(Args.steps):
	score = Args.score + k*Args.delta
	s = Args.scorefmt % (10**(-score))
	E = get_P(score, EPQ_score)
	if E < 0.001:
		s += "\t~0"
	elif E > 10:
		s += "\t>10"
	else:
		if E == 0:
			s += "\t0"
		elif E < 1e-3:
			s += "\t%.2e" % E
		else:
			s += "\t%.4g" % E
	P = get_P(score, P_T_score)
	if P > 0.99:
		s += "\t~1"
	else:
		s += "\t%.6f" % P
	print(s)
# print('# ' + ' '.join(sys.argv))