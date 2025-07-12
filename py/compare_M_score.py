#!/usr/bin/python3

import sys
import math
import argparse
import numpy as np
from read_dist import read_dist

AP = argparse.ArgumentParser()
AP.add_argument("--edf1", required=True)
AP.add_argument("--edf2", required=True)
Args = AP.parse_args()

# def read_dist(fn, distname):
# 	bin_mids = []
# 	fld_nr = None
# 	v = []
# 	for line in open(fn):
# 		if line.startswith('#'):
# 			continue
# 		if fld_nr is None:
# 			hdr = line[:-1].split('\t')
# 			assert hdr[0] == "binmids"
# 			for i in range(len(hdr)):
# 				if hdr[i] == distname:
# 					fld_nr = i
# 					break
# 			if fld_nr is None:
# 				assert False, "distname=%s not found in fn=%s" % (distname, fn)
# 			continue
# 		if len(line.strip()) == 0:
# 			continue
# 		flds = line[:-1].split('\t')
# 		bin_mid = float(flds[0])
# 		x = float(flds[fld_nr])

# 		bin_mids.append(bin_mid)
# 		v.append(x)

# 	return bin_mids, np.array(v, dtype=np.float32)

bin_mids1, M_score1 = read_dist(Args.edf1, "M_score")
bin_mids2, M_score2 = read_dist(Args.edf2, "M_score")
assert bin_mids1 == bin_mids2

for binidx in range(len(bin_mids1)):
	score = bin_mids1[binidx]
	M1 = M_score1[binidx]
	M2 = M_score2[binidx]
	s = "%.3g" % score
	s += "\t%d" % M1
	s += "\t%d" % M2
	s += "\t%.3g" % (M2/(M1+0.1))
	s += "\t%.3g" % (M1/(M2+0.1))
	print(s)