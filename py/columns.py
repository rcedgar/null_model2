#!/usr/bin/python3

import sys

File = sys.stdin

if len(sys.argv) > 1:
	FileName = sys.argv[1]
	File = open(FileName)

Lines = []
MaxColSizes = []
while 1:
	Line = File.readline()
	if len(Line) == 0:
		break

	Line = Line.strip()
	Lines.append(Line)
	Fields = Line.split('\t')
	for i in range(0, len(Fields)):
		f = Fields[i]
		if i >= len(MaxColSizes):
			MaxColSizes.append(0)
		n = len(f)
		if n > MaxColSizes[i]:
			MaxColSizes[i] = n

for Line in Lines:
	Fields = Line.split('\t')
	s = ""
	for i in range(0, len(Fields)):
		if i > 0:
			s += "  "
		f = Fields[i]
		n = MaxColSizes[i]
		s += "%*.*s" % (n, n, f)
	print(s)
