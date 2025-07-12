#!/usr/bin/python3

import sys

hitsfn = sys.argv[1]

doms = set( [ line.split('\t')[0] for line in open("../data/scop40c.lookup") ] )

N = 0
n = 0
for line in open(hitsfn):
	flds = line.split('\t')
	q = flds[0]
	t = flds[1]
	N += 1
	if t in doms and q in doms:
		n += 1
		sys.stdout.write(line)

sys.stderr.write("%d / %d SCOP40c hits %s\n" % (n, N, hitsfn))