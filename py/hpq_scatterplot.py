import sys
import re
import math
import argparse
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from pymoo.algorithms.soo.nonconvex.pattern import PatternSearch
from pymoo.optimize import minimize
from pymoo.core.problem import Problem

AP = argparse.ArgumentParser()
AP.add_argument('--edfs', required=True, nargs='+')
AP.add_argument('--labels', required=True, nargs='+')
AP.add_argument('--plot', help="Plot file(s), default none")
AP.add_argument('--prefilter_size', type=int, required=True)
AP.add_argument('--xrange', default="1000:1e9")
AP.add_argument('--yrange', default="1e-3:100")
AP.add_argument('--output', default="/dev/stdout")
AP.add_argument('--title')
Args = AP.parse_args()

assert len(Args.edfs) == len(Args.labels)

matplotlib.use('Agg')

fout = open(Args.output, "w")

flds = Args.xrange.replace('_', '-').split(':')
assert len(flds) == 2
xlim = [ float(flds[0]), float(flds[1]) ]

flds = Args.yrange.replace('_', '-').split(':')
assert len(flds) == 2
ylim = [ float(flds[0]), float(flds[1]) ]

db2size = {}
db2size["afdb50"] = 53665860
db2size["scop40.n2"] = 11211/2
db2size["scop40.n4"] = 11211/4
db2size["scop40"] = 11211
db2size["scop95"] = 28284
db2size["scop40x2"] = 11211*2
db2size["scop40x4"] = 11211*4
db2size["scop40x8"] = 11211*8
db2size["cath40"] = 34653
db2size["bfvd"] = 347514
db2size["pdb"] = 884129
db2size["scop95.cluster40"] = 15696
db2size["scop95.cluster70"] = 22188

names = set(db2size.keys())
mul_names = set([ "scop40.n2", "scop40.n4", "scop40x2", "scop40x4", "scop40x8", "scop95.cluster40", "scop95.cluster70" ])
other_names = [ "pdb", "afdb50", "bfvd", "cath40", "scop95", "scop40" ]

def get_dbname_from_edf_fn(fn):
	trace = (fn == "../edf/reseek.scop40x8")
	for name in mul_names:
		pos = fn.find(name)
		if pos >= 0:
			return name
	for name in other_names:
		pos = fn.find(name)
		if pos >= 0:
			return name
	assert False, "get_dbname_from_edf_fn(%s)" % fn

Ds = []
Hs = []
log10Ds = []
log10Hs = []
for fn in Args.edfs:
	HPQ = None
	dbname = get_dbname_from_edf_fn(fn)
	D = db2size[dbname]
	H = None
	for line in open(fn):
		if line.find("HPQ=") > 0:
			M = re.search(r"HPQ=([0-9.e]+)", line)
			if M is None:
				assert False, "re failed '%s'\n" % line
			H = float(M.group(1))
	assert not H is None
	Ds.append(D)
	Hs.append(H)

	log10Ds.append(math.log10(D))
	log10Hs.append(math.log10(H))

def logistic(offset, scale, norm, x):
	effective_x = scale*(x - offset)
	y = norm/(1 + math.exp(-effective_x))
	return y

def rmse(offset, scale, norm):
	sumd2 = 0
	for i in range(len(log10Ds)):
		x = log10Ds[i]
		y = log10Hs[i]
		yhat = logistic(offset, scale, norm, x)
		d = yhat - y
		sumd2 += d*d
	return math.sqrt(sumd2)

# offset, scale, norm
xls = [ -6,		0.01]
xus = [ 6,		10]

initial_offset = 0
initial_scale = 0.1

thenorm = math.log10(Args.prefilter_size)
rmse_initial = rmse(initial_offset, initial_scale, thenorm)

class Fit(Problem):
	def __init__(self):
		# vars: offset, scale, 
		super().__init__(n_var=2,
				   n_obj=1,
				   n_constr=0,
				   xl = xls,
				   xu = xus)

	def _evaluate(self, x, out, *args, **kwargs):
		n = len(x)
		ys = []
		for i in range(n):
			assert len(x[i]) == 2
			offset = x[i][0]
			scale = x[i][1]
			y = rmse(offset, scale, thenorm)
			ys.append(y)
		out["F"] = ys

res = minimize(Fit(),
			   PatternSearch(),
			   verbose=False,
			   seed=1)

offset, scale = res.X
rmse_final = res.F

rmse_final = rmse(offset, scale, thenorm)

for i in range(len(log10Ds)):
	x = log10Ds[i]
	y = log10Hs[i]
	yhat = logistic(offset, scale, thenorm, x)
	Hhat = 10**yhat

	s = "%.3g" % x
	s += "\t%.3g" % y
	s += "\t%.3g" % yhat
	s += "\t%.3g" % Ds[i]
	s += "\t%.3g" % Hs[i]
	s += "\t%.3g" % Hhat
	s += "\t%s" % Args.labels[i]
	fout.write(s + '\n')

fig, ax = plt.subplots(1, 1)
ax.set_title(Args.title)
ax.set_xlabel("Database size")
ax.set_ylabel("Avg. hits per query")
ax.set_yscale('log')
ax.set_xscale('log')
ax.set_xlim(xlim)
ax.set_ylim(ylim)

plotDs = []
plotHfits = []
D = xlim[0]
while D <= xlim[1]:
	plotDs.append(D)
	yhat = logistic(offset, scale, thenorm, math.log10(D))
	Hhat = 10**yhat
	plotHfits.append(Hhat)
	D *= 2

ax.scatter(Ds, Hs)
ax.plot(plotDs, plotHfits, color = "orange", linestyle = "dotted")

for i, label in enumerate(Args.labels):
	ax.annotate(label, (Ds[i], Hs[i]))

ax.figure.set_size_inches(4, 3)
fig.tight_layout()

if not Args.plot is None:
	fns = Args.plot.split(',')
	for fn in fns:
		sys.stderr.write(fn + '\n')
	fig.savefig(fn)

s = f"{rmse_initial=:.2g}"
s += f" {rmse_final=:.2g} {offset=:.3g} {scale=:.3g} {thenorm=:.3g}"
fout.write("# " + s + "\n")

fout.close()