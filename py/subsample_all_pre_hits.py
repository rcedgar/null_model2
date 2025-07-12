#!/usr/bin/python3

import sys
import random
import argparse
import os

AP = argparse.ArgumentParser()
AP.add_argument("--hits_all", required=True)
AP.add_argument("--hits_pre", required=True)
AP.add_argument("--out_all", required=True)
AP.add_argument("--out_pre", required=True)
AP.add_argument("--flip_fast", default=False, action="store_true")
AP.add_argument("--sample", type=int, default=1000)
Args = AP.parse_args()

fall = open(Args.out_all, "w")
fpre = open(Args.out_pre, "w")

pairs = set()

N = 0
n = 0
total = 0
filesize = os.path.getsize(Args.hits_all)
for line in open(Args.hits_all):
	N += 1
	total += len(line) + 1
	if random.randint(0, 5915587277)%Args.sample != 0:
		continue
	if n%100 == 0:
		pct = total*100/filesize
		sys.stderr.write("%d %.3g%%\r" % (n, pct))
	n += 1
	flds = line[:-1].split('\t')
	q = flds[0].split('/')[0]
	t = flds[1].split('/')[0]
	if q == "query":
		continue
	pair = (q, t)
	pairs.add(pair)
	fall.write(line)
fall.close()

sys.stderr.write("%d/%d = %.1f (%.1f)\n" % (N, n, N/n, Args.sample))

found = 0
for line in open(Args.hits_pre):
	if found%100 == 0:
		sys.stderr.write("%d\r" % found)

	flds = line[:-1].split('\t')
	q = flds[0].split('/')[0]
	t = flds[1].split('/')[0]
	if Args.flip_fast:
		pair = (t, q)
	else:
		pair = (q, t)
	if not pair in pairs:
		continue
	if Args.flip_fast:
		fpre.write(line = t + '\t' + q + '\t'.join(flds[2:]))
	else:
		fpre.write(line)
	found += 1
fpre.close()

sys.stderr.write("%d/%d found\n" % (found, len(pairs)))
