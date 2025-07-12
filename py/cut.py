#!/usr/bin/python3

import sys

sns = sys.argv[1]
Fields = sns.split(',')

ns = []
for Field in Fields:
	n = int(Field)
	ns.append(n)

f = sys.stdin
if len(sys.argv) > 2:
	f = open(sys.argv[2])

while 1:
	Line = f.readline()
	if len(Line) == 0:
		break

	Fields = Line[:-1].split('\t')
	s = ""
	for n in ns:
		if s != "":
			s += '\t'
		s += Fields[n-1]
	print(s)
