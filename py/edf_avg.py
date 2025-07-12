#!/usr/bin/python3

import sys
import statistics
from plot_dists_lib import read_dist

fns = sys.argv[1:]
nrfiles = len(fns)

# score   NT      NF      CDF(score)      CDF(score|T)    CDF(score|F)    P(T|score)      P(T|score)B     CDF(T|score)           CDF(T|score)B   P(F|score)      CDF(F|score)    P(score|T)      P(score|F)

scores = []
with open(fns[0]) as file:
	hdrline0 = file.readline()
	assert len(hdrline0) > 0, "fn0=%s\n" % fns[0]
	names = hdrline0[:-1].split('\t')
	# assert names[0] == "binmids"
	scores = [ line.split('\t')[0] for line in file if not line.startswith('#') ]
distnames = names[1:]
nrdists = len(distnames)

distname2score2values = {}
for distname in distnames:
	distname2score2values[distname] = {}
	for score in scores:
		distname2score2values[distname][score] = []

for fn in fns:
	with open(fn) as file:
		hdrline = file.readline()
		assert len(hdrline) > 0, "fn=%s\n" % fn
		if hdrline != hdrline0:
			sys.stderr.write("hdrline='%s'\n" % hdrline[:-1])
			sys.stderr.write("hdrline0='%s'\n" % hdrline0[:-1])
			sys.stderr.write("fn0='%s' fn=%s\n" % (fns[0], fn))
			assert False
		names = hdrline[:-1].split('\t')
		assert names[1:] == distnames
		scoreidx = 0
		for line in file:
			if line.startswith('#'):
				continue
			flds = line[:-1].split('\t')
			score = flds[0]
			if score != scores[scoreidx]:
				sys.stderr.write('\n')
				sys.stderr.write('fn0=' + fns[0] + '\n')
				sys.stderr.write('fn =' + fn + '\n')
				sys.stderr.write('idx=%d\n' % scoreidx)
				sys.stderr.write("score0='%s' score='%s'\n" \
					% (score, scores[scoreidx]))
				assert False
			for i in range(nrdists):
				value = float(flds[1+i])
				distname2score2values[distnames[i]][score].append(value)
			scoreidx += 1

sys.stdout.write(hdrline0)
for score in scores:
	s = score
	for distname in distnames:
		values = distname2score2values[distname][score]
		assert len(values) == nrfiles
		meanvalue = statistics.mean(values)
		s += "\t%.3g" % meanvalue
	sys.stdout.write(s + '\n')
