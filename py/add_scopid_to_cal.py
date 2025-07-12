#!/usr/bin/python3

import sys

calfn = sys.argv[1]
lookupfn = sys.argv[2]

dom2scopid = {}
for line in open(lookupfn):
	flds = line[:-1].split('\t')
	dom = flds[0]
	scopid = flds[1]
	dom2scopid[dom] = scopid

skip = False
for line in open(calfn):
	if line.startswith('>'):
		dom = line[1:-1]
		scopid = dom2scopid.get(dom, None)
		if scopid is None:
			skip = True
			continue
		else:
			skip = False
			sys.stdout.write(line[:-1] + '/' + scopid + '\n')
	else:
		if not skip:
			sys.stdout.write(line)
