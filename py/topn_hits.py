#!/usr/bin/python3

import sys
import math
import argparse

AP = argparse.ArgumentParser()
AP.add_argument("--sorted_hits", required=True)
AP.add_argument("--qfield", required=False, type=int, default=1)
AP.add_argument("--tfield", required=False, type=int, default=2)
AP.add_argument("--scorefield", required=False, type=int, default=3)
AP.add_argument("--n", required=False, type=int, default=32)
Args = AP.parse_args()

qidx = Args.qfield - 1
tidx = Args.tfield - 1
sidx = Args.scorefield - 1

currq = None
currn = 0
done_qs = set()
for line in open(Args.sorted_hits):
	flds = line[:-1].split('\t')
	q = flds[qidx]
	t = flds[tidx]
	s = flds[sidx]
	if q != currq:
		assert not q in done_qs
		done_qs.add(q)
		currq = q
		n = 0
	if n < Args.n:
		print(q + '\t' + t + '\t' + s)
		n += 1
