import random

tsvfn = "/mnt/c/src/null_model/big_hits/blastpx.scop40"

N = 1000

pairs = []
for line in open(tsvfn):
	flds = line[:-1].split('\t')
	if flds[0] == flds[1]:
		continue
	native = float(flds[2])
	loglin = float(flds[4])
	if native < 1e-10 or loglin < 1e-10:
		continue
	if native > 1 or loglin > 1:
		continue
	pairs.append((native, loglin))

random.shuffle(pairs)

for native, loglin in pairs[:N]:
	print("%.3g\t%.3g" % (native, loglin))
