import sys

fn = sys.argv[1]

fldidx = 4
lo = 0.05
hi = 1.05

for line in open(fn):
	flds = line[:-1].split('\t')
	ts = float(flds[fldidx])
	if ts >= lo and ts <= hi:
		sys.stdout.write(line)
