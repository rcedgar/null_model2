#!/usr/bin/python3

import sys
import math
import dbname2size
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy import stats

matplotlib.use('Agg')

searchdbs = [ "scop40", "bfvd", "pdb", "afdb50" ]

# reseek_ts_hitrates.bash

# reseek sensitive SCOP40 vs AFDB50 1192998855 hits
#	hitrate = 1192998855/(11211*53665860) = 0.00198

# Hit rates
mode_searchdb2h = {}

mode_searchdb2h[ ("fast", "scop40") ]		= 0.00239
mode_searchdb2h[ ("sensitive", "scop40") ] = 0.00537

mode_searchdb2h[ ("fast", "bfvd") ]		= 4.33e-05
mode_searchdb2h[ ("sensitive", "bfvd") ]	= 0.00302

mode_searchdb2h[ ("fast", "pdb") ]			= 0.000319
mode_searchdb2h[ ("sensitive", "pdb") ]	= 0.0047

mode_searchdb2h[ ("fast", "afdb50") ]      = 2e-05
mode_searchdb2h[ ("sensitive", "afdb50") ] = 0.00198

# Log-linear fits to CDF(score|F)
refdb2_C_score_F_mc = {}
refdb2_C_score_F_mc["scop40"] = (14.68, 0.008205)
refdb2_C_score_F_mc["scop40c"] = (20.19, -0.4998)

# Log-linear fits to CDF(prefilter)
searchdb_refdb2prefilter_mc = {}
searchdb_refdb2prefilter_mc[ ("afdb50", "scop40") ] = (-8.768, -2.135)
searchdb_refdb2prefilter_mc[ ("afdb50", "scop40c") ] = (-15.79, -1.357)

searchdb_refdb2prefilter_mc[ ("bfvd", "scop40") ] = (-12.47, 0.03332)
searchdb_refdb2prefilter_mc[ ("bfvd", "scop40c") ] = (-20.3, 1.059)

searchdb_refdb2prefilter_mc[ ("pdb", "scop40") ] = (-12.13, -0.3027)
searchdb_refdb2prefilter_mc[ ("pdb", "scop40c") ] = (-19.1, 0.5284)

searchdb_refdb2prefilter_mc[ ("scop40", "scop40") ] = (-13.24, 0.2555)
searchdb_refdb2prefilter_mc[ ("scop40", "scop40c") ] = (-20.54, 1.171)

fh = open("reseek_calibrate.h", "w")

for searchdb in searchdbs:
	fh.write("dbsize(%s, %d)\n" % (searchdb, dbname2size.dbname2size[searchdb]))

for mode in [ "fast", "sensitive" ]:
	for searchdb in searchdbs:
		h = mode_searchdb2h[ (mode, searchdb) ]
		fh.write("hitrate(%s, %s, %.3g)\n" % (mode, searchdb, h))

for refdb in [ "scop40", "scop40c" ]:
	m, c = refdb2_C_score_F_mc[refdb]
	fh.write("C_score_F_mc(%s, %.3g, %.3g)\n" % (refdb, m, c))

for searchdb in searchdbs:
	for refdb in [ "scop40", "scop40c" ]:
		m, c = searchdb_refdb2prefilter_mc[ (searchdb, refdb) ]
		fh.write("prefilter_mc(%s, %s, %.3g, %.3g)\n" % \
			(searchdb, refdb, m, c))

		m = None
		c = None

fh.close()

def calc_evalue_reseekv25(ts, dbsize):
	a = 5.0
	b = -40.0
	logE = a + b*ts
	E_scop = math.exp(logE)/11211
	E = E_scop*dbsize
	return E

def estimate_PF(mode, searchdb):
	if mode == "fast":
		return 0.5
	else:
		return 1

def get_hitrate(mode, searchdb):
	h = mode_searchdb2h.get((mode, searchdb))
	if h is None:
		assert False, "get_hitrate(%s, %s)\n" % (mode, searchdb)
	return h

def get_C_score_F_mc(refdb):
	mc = refdb2_C_score_F_mc.get(refdb)
	if mc is None:
		assert False, "get_C_score_F_mc(%s)\n" % (refdb)
	return mc

def get_CDF_prefilter_mc(searchdb, refdb):
	mc = searchdb_refdb2prefilter_mc.get((searchdb, refdb))
	if mc is None:
		assert False, "get_CDF_prefilter_mc(%s, %s)\n" % (searchdb, refdb)
	return mc

def get_loglin_C_score_F(ts, m, c):
	logCDF = m*ts + c
	return min(10**(-logCDF), 1)

def get_loglin_CDF_prefilter(ts, m, c):
	logCDF = m*ts + c
	return min(10**logCDF, 1)

def estimate_evalue(ts, mode, searchdb, refdb):
	D = dbname2size.dbname2size[searchdb]
	PF = estimate_PF(mode, searchdb)
	h = get_hitrate(mode, searchdb)
	C_score_F_m, C_score_F_c = get_C_score_F_mc(refdb)
	C_score_F = get_loglin_C_score_F(ts, C_score_F_m, C_score_F_c)
	if mode == "fast":
		CDF_prefilter_m, CDF_prefilter_c = get_CDF_prefilter_mc(searchdb, refdb)
		CDF_prefilter = get_loglin_CDF_prefilter(ts, CDF_prefilter_m, CDF_prefilter_c)
		evalue = D*h*PF*CDF_prefilter
	elif mode == "sensitive":
		evalue = D*h*PF*C_score_F
	else:
		assert False, "mode=" + mode
	return evalue

sys.stderr.write("evalue.tsv\n")
f = open("evalue.tsv", "w")
s = "TS"
for searchdb in searchdbs:
	for refdb in [ "", "c" ]:
		for mode in [ "f", "s" ]:
			s += "\t" + searchdb + refdb + "/" + mode
f.write(s + '\n')

edict = {}
for searchdb in searchdbs:
	for refdb in [ "scop40", "scop40c" ]:
		for mode in [ "fast", "sensitive" ]:
			edict[(searchdb, refdb, mode)] = []

ts_values = []
for binidx in range(0, 21):
	ts = 0.05 + binidx*0.05
	ts_values.append(ts)
	s = "%.2f" % ts
	for searchdb in searchdbs:
		for refdb in [ "scop40", "scop40c" ]:
			for mode in [ "fast", "sensitive" ]:
				evalue = estimate_evalue(ts, mode, searchdb, refdb)
				edict[(searchdb, refdb, mode)].append(evalue)
				s += "\t%.3g" % evalue
	f.write(s + '\n')
f.close()

e25s = []
for binidx in range(0, 21):
	ts = 0.05 + binidx*0.05
	evalue = calc_evalue_reseekv25(ts, 11211)
	e25s.append(evalue)
edict[("scop40", "scop40", "v25")] = e25s

sys.stderr.write("C_score_F.tsv\n")
f = open("C_score_F.tsv", "w")
s = "TS"
s += "\tSCOP40"
s += "\tSCOP40c"
f.write(s + '\n')

for binidx in range(0, 21):
	ts = 0.05 + binidx*0.05
	s = "%.2f" % ts
	for refdb in [ "scop40", "scop40c" ]:
		C_score_F_m, C_score_F_c = get_C_score_F_mc(refdb)
		C_score_F = get_loglin_C_score_F(ts, C_score_F_m, C_score_F_c)
		s += "\t%.3g" % C_score_F
	f.write(s + '\n')
f.close()

sys.stderr.write("CDF_prefilter.tsv\n")
f = open("CDF_prefilter.tsv", "w")
s = "TS"
for searchdb in searchdbs:
	for refdb in [ "", "c" ]:
		s += "\t" + searchdb + refdb
f.write(s + '\n')

for binidx in range(0, 21):
	ts = 0.05 + binidx*0.05
	s = "%.2f" % ts
	for searchdb in searchdbs:
		for refdb in [ "scop40", "scop40c" ]:
			CDF_prefilter_m, CDF_prefilter_c = get_CDF_prefilter_mc(searchdb, refdb)
			CDF_prefilter = get_loglin_CDF_prefilter(ts, CDF_prefilter_m, CDF_prefilter_c)
			s += "\t%.3g" % CDF_prefilter
	f.write(s + '\n')
f.close()

nrsearchdbs = len(searchdbs)

fig, axs = plt.subplots(1, nrsearchdbs)

for idx in range(nrsearchdbs):
	searchdb = searchdbs[idx]
	ax = axs[idx]
	# if searchdb == "scop40":
	# 	evalues25 = edict[("scop40", "scop40", "v25")]
	# 	ax.plot(ts_values, evalues25, label="v2.5", \
	# 		color="gray", linestyle="dashdot")
	for refdb in [ "scop40", "scop40c" ]:
		for mode in [ "fast", "sensitive" ]:
			evalues = edict[(searchdb, refdb, mode)]
			if mode == "fast":
				color = "orange"
			elif mode == "sensitive":
				color = "blue"
			else:
				assert False
			if refdb == "scop40":
				label = mode
				linestyle = "solid"
			elif refdb == "scop40c":
				label = mode + "(c)"
				linestyle = "dashed"
			else:
				assert False
			ax.plot(ts_values, evalues, label=label, \
				color=color, linestyle=linestyle)

	if searchdb == "scop40":
		ax.set_title("SCOP40 (10k)")
	elif searchdb == "bfvd":
		ax.set_title("BFVD (350k)")
	elif searchdb == "pdb":
		ax.set_title("PDB (1M)")
	elif searchdb == "afdb50":
		ax.set_title("AFDB50 (50M)")
	ax.set_yscale('log')
	ax.set_xlabel("TS")
	ax.set_xlim([0.25, 0.75])
	ax.set_ylim([1e-9, 10])
	ax.set_ylabel("Estimated E-value")
	ax.legend()

fig.set_size_inches(12, 3)
fig.tight_layout()

fn = "reseek_calibrate.svg"
sys.stderr.write(fn + '\n')
fig.savefig(fn)

fn = "reseek_calibrate.png"
sys.stderr.write(fn + '\n')
fig.savefig(fn)

fig, axs = plt.subplots(1, 3)

dbsizes = []
ms = []
cs = []
m2s = []
c2s = []
hs = []
h2s = []
for idx in range(nrsearchdbs):
	searchdb = searchdbs[idx]
	dbsize = dbname2size.dbname2size[searchdb]

	h = mode_searchdb2h[ ("fast", searchdb) ]
	h2 = mode_searchdb2h[ ("sensitive", searchdb) ]

	m, c = searchdb_refdb2prefilter_mc[ (searchdb, "scop40") ]
	m2, c2 = searchdb_refdb2prefilter_mc[ (searchdb, "scop40c") ]

	dbsizes.append(dbsize)

	hs.append(h)
	h2s.append(h2)

	ms.append(m)
	cs.append(c)

	m2s.append(m2)
	c2s.append(c2)

xlabels = []
for x in searchdbs:
	xlabels.append(x.upper())

axs[0].plot(dbsizes, hs, linewidth=1, marker='o', label="fast")
axs[0].plot(dbsizes, h2s, linewidth=1, marker='o', label="sensitive")
axs[0].set_xscale('log')
axs[0].set_yscale('log')
axs[0].legend()
axs[0].set_ylim([1e-6, 5e-2])
axs[0].set_title("Hit-rate h")
axs[0].set_xlabel("DB size")
axs[0].set_ylabel("h")
axs[0].set_xticks(dbsizes)
axs[0].set_xticklabels(xlabels, rotation=270, fontsize=10)

axs[1].plot(dbsizes, ms, linewidth=1, marker='o', label="scop40")
axs[1].plot(dbsizes, m2s, linewidth=1, marker='o', label="scop40c")
axs[1].set_xscale('log')
axs[1].legend()
axs[1].set_title("CDF(prefilter) m")
axs[1].set_xlabel("DB size")
axs[1].set_ylabel("m")
axs[1].set_ylim([-25, -5])
axs[1].set_xticks(dbsizes)
axs[1].set_xticklabels(xlabels, rotation=270, fontsize=10)

axs[2].plot(dbsizes, cs, linewidth=1, marker='o', label="scop40")
axs[2].plot(dbsizes, c2s, linewidth=1, marker='o', label="scop40c")
axs[2].set_xscale('log')
axs[2].set_ylim([2, -3])
axs[2].legend()
axs[2].set_title("CDF(prefilter) c")
axs[2].set_xlabel("DB size")
axs[2].set_ylabel("c")
axs[2].set_xticks(dbsizes)
axs[2].set_xticklabels(xlabels, rotation=270, fontsize=10)

fig.set_size_inches(9, 3)
fig.tight_layout()

fn = "reseek_calibrate_mch.svg"
sys.stderr.write(fn + '\n')
fig.savefig(fn)

fn = "reseek_calibrate_mch.png"
sys.stderr.write(fn + '\n')
fig.savefig(fn)

sys.exit(0)

##################################################################################
# Too much fitting, keep this just in case I change my mind
##################################################################################
def final_fit_linscale(ys, use, name, fn):
	ys_to_fit = []
	logdbsizes_to_fit = []
	for i in range(len(use)):
		if use[i]:
			ys_to_fit.append(ys[i])
			logdbsizes_to_fit.append(math.log10(dbsizes[i]))

	m, c, r_value, p_value, std_err = \
		stats.linregress(logdbsizes_to_fit, ys_to_fit)

	f = open(fn, "w")
	f.write("y=%s  m=%.3g   c=%.3g\n" % (name, m, c))
	f.write("%8.8s  %8.8s  %8.8s  %8.8s\n" % ("y", "logsize", "10^logsz", "y_fit"))
	for i in range(len(logdbsizes_to_fit)):
		y = ys[i]
		logsize = logdbsizes_to_fit[i]
		y_fit = m*logsize + c
		f.write("%8.3g  %8.3g  %8.3g  %8.3g\n" % (y, logsize, 10**logsize, y_fit))
	f.close()

def final_fit_logscale(ys, use, name, fn):
	logys = []
	logdbsizes_to_fit = []
	for i in range(len(use)):
		if use[i]:
			logys.append(math.log10(ys[i]))
			logdbsizes_to_fit.append(math.log10(dbsizes[i]))

	m, c, r_value, p_value, std_err = \
		stats.linregress(logdbsizes_to_fit, logys)

	f = open(fn, "w")
	f.write("y=%s  m=%.3g   c=%.3g\n" % (name, m, c))
	f.write("%8.8s  %8.8s  %8.8s  %8.8s\n" % ("y", "logsize", "10^logsz", "y_fit"))
	for i in range(len(logdbsizes_to_fit)):
		y = ys[i]
		logsize = logdbsizes_to_fit[i]
		logy_fit = m*logsize + c
		y_fit = 10**logy_fit
		f.write("%8.3g  %8.3g  %8.3g  %8.3g\n" % (y, logsize, 10**logsize, y_fit))
	f.close()

final_fit_logscale(hs, [ True, False, True, True ], "h", "h_fit.tsv")
final_fit_linscale(ms, [ True, True, True, True ], "m", "m_fit.tsv")
final_fit_linscale(cs, [ False, True, True, True ], "c", "c_fit.tsv")

final_fit_logscale(h2s, [ True, False, True, True ], "h2", "h2_fit.tsv")
final_fit_linscale(m2s, [ True, True, True, True ], "m2", "m2_fit.tsv")
final_fit_linscale(c2s, [ False, True, True, True ], "c2", "c2_fit.tsv")
