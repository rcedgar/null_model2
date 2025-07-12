import sys

fn = sys.argv[1]

qs = set()
q2n = {}

for line in open(fn):
	flds = line[:-1].split('\t')
	q = flds[0]
	t = flds[1]

	if not q in qs:
		qs.add(q)
		q2n[q] = 0
	q2n[q] += 1

qs = list(qs)
ns = [ q2n[q] for q in qs ]
order = sorted(range(len(qs)), key=ns.__getitem__, reverse=True)

for i in order:
	q = qs[i]
	n = q2n[q]
	print("%d\t%s" % (n, q))
