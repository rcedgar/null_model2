#!/usr/bin/python3

import sys
import math
import argparse

AP = argparse.ArgumentParser()
AP.add_argument("--tophits", required=True)
AP.add_argument("--fasthits", required=True)
AP.add_argument("--qfield", type=int, default=1)
AP.add_argument("--tfield", type=int, default=2)
Args = AP.parse_args()

qidx = Args.qfield - 1
tidx = Args.tfield - 1

q2tophits_set = {}
q2tophits_list = {}
q2foundhits_set = {}
currq = None
currn = 0
done_qs = set()
sys.stderr.write(Args.tophits + " ...")
for line in open(Args.tophits):
	flds = line[:-1].split('\t')
	q = flds[0].split('/')[0]
	t = flds[1]
	if q != currq:
		assert not q in done_qs
		currq = q
		done_qs.add(q)
		q2tophits_set[q] = set()
		q2tophits_list[q] = []
		q2foundhits_set[q] = set()
	q2tophits_set[q].add(t)
	q2tophits_list[q].append(t)
sys.stderr.write("\n")

fast_but_not_top = 0
linenr = 0
for line in open(Args.fasthits):
	linenr += 1
	if linenr%1000 == 0:
		sys.stderr.write("%d\r" % linenr)
	flds = line[:-1].split('\t')
	q = flds[qidx].split('/')[0]
	if not q in done_qs:
		fast_but_not_top += 1
		continue
	t = flds[tidx]
	if t in q2tophits_set[q]:
		q2foundhits_set[q].add(t)
sys.stderr.write("%d\n" % linenr)

sys.stderr.write("fast_but_not_top=%d\n" % fast_but_not_top)

rank_to_count = [0]*32
rank_to_foundcount = [0]*32

for q in done_qs:
	tophits_list = q2tophits_list[q][:32]
	foundhits_set = q2foundhits_set[q]
	for rank in range(len(tophits_list)):
		rank_to_count[rank] += 1
		t = tophits_list[rank]
		if t in foundhits_set:
			rank_to_foundcount[rank] += 1

for rank in range(32):
	print("%d\t%d\t%d" % (rank, rank_to_count[rank], rank_to_foundcount[rank]))
