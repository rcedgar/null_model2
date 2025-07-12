#!/usr/bin/python3

# reseek_calibrate_v2.py is re-write of reseek_calibrate.py to:
#	(a) read parameters from edfs, loglins
#	(b) validate E-value vs. FPEPQ for SCOP40 fast and sensitive

import re
import sys
import math
import dbname2size
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy import stats
from read_dist import read_dist

matplotlib.use('Agg')

modes = [ "fast", "sensitive" ]
refdbs = [ "scop40", "scop40c" ]
searchdbs = [ "scop40", "bfvd", "pdb", "afdb50" ]

###############################################################
# Measured FPEPQ on SCOP40
###############################################################
mode_refdb2FPEPQ_tss = {}
mode_refdb2FPEPQ = {}
for mode in modes:
	for refdb in refdbs:
		edffn = "../edf/reseek_sensitive_ts.scop40.scop40." + refdb
		mode_refdb2FPEPQ_tss[ (mode, refdb) ], mode_refdb2FPEPQ[ (mode, refdb) ] = read_dist(edffn, "cve_epq")

def get_measured_FPEPQ(ts, mode, refdb):
	binmids = mode_refdb2FPEPQ_tss[(mode, refdb)]
	FPEPQs = mode_refdb2FPEPQ[(mode, refdb)]
	FPEPQ = np.interp(ts, binmids, FPEPQs)
	return FPEPQ

###############################################################
# Measured C_score_F (use sensitive, fast varies due to filter)
###############################################################
refdb2C_score_F = {}
refdb2C_score_F_binmids = {}
for refdb in refdbs:
	edffn = "../edf/reseek_sensitive_ts.scop40.scop40." + refdb
	refdb2C_score_F_binmids[refdb], refdb2C_score_F[refdb] = read_dist(edffn, "C_score_F")

def get_measured_C_score_F(ts, refdb):
	binmids = refdb2C_score_F_binmids[refdb]
	C_score_Fs = refdb2C_score_F[refdb]
	C_score_F = np.interp(ts, binmids, C_score_Fs)
	return C_score_F

###############################################################
# Measured CDF_prefilter = CDF(pass prefilter and FP | TS)
# Dependency on refdb via P(TS | FP)
###############################################################
searchdb_refdb2CDF_prefilter_tss = {}
searchdb_refdb2CDF_prefilter = {}
for searchdb in searchdbs:
	for refdb in refdbs:
		tss = []
		cdfs = []
		if refdb == "scop40":
			cdffn = "../P_prefilter/" + searchdb + "_cdf.tsv"
		else:
			cdffn = "../P_prefilter/" + searchdb + "_c_cdf.tsv"
		f = open(cdffn)
		hdr = f.readline()
		assert hdr.startswith("newts\tP_score_F")
		for line in f:
			if line.startswith('#'):
				continue
			flds = line[:-1].split('\t')
			assert len(flds) == 4
			tss.append(float(flds[0]))
			cdfs.append(float(flds[3]))
		f.close()
		searchdb_refdb2CDF_prefilter[ (searchdb, refdb) ] = cdfs
		searchdb_refdb2CDF_prefilter_tss[ (searchdb, refdb) ] = tss

def get_measured_CDF_prefilter(searchdb, refdb, ts):
	cdfs = searchdb_refdb2CDF_prefilter[ (searchdb, refdb) ]
	tss = searchdb_refdb2CDF_prefilter_tss[ (searchdb, refdb) ]
	cdf = np.interp(ts, tss, cdfs)
	return cdf

##############################################################
# Hit rates
# Difference between SCOP40 and SCOP40c negligible:
#	reseek_fast_ts.scop40.scop40.scop40:	hitrate=0.00239
#	reseek_fast_ts.scop40.scop40.scop40c:	hitrate=0.00255
##############################################################
mode_searchdb2h = {}
for searchdb in searchdbs:
	for mode in modes:
	# reseek sensitive SCOP40 vs AFDB50 1192998855 hits
	#	hitrate = 1192998855/(11211*53665860) = 0.00198
		if mode == "sensitive" and searchdb == "afdb50":
			h = 0.00198
		else:
			if searchdb == "scop40":
				refdb = "scop40"
			else:
				refdb = "none"
			edffn = "../edf/reseek_" + mode + "_ts.scop40." + searchdb + "." + refdb
			f = open(edffn)
			h = None
			for line in f:
				M = re.search(r"hitrate=([0-9.e+-]+)", line)
				if not M is None:
					h = float(M.group(1))
					break
			f.close()
			assert not h is None, "hitrate= not found in edffn=" + edffn
		mode_searchdb2h[ (mode, searchdb) ] = h

##############################################################
# Log-linear fits to CDF(score|F)
##############################################################
refdb2_C_score_F_mc = {}
for refdb in refdbs:
	loglinfn = "../fit_loglin/reseek_ts." + refdb + ".tsv"
	f = open(loglinfn)
	line = f.readline()
	f.close()
	# m=14.68, c=0.008205
	M = re.search(r"m=([0-9.e+-]+).*c=([0-9.e+-]+)", line)
	assert not M is None, "m=, c= not found in edffn=" + loglinfn
	m = float(M.group(1))
	c = float(M.group(2))
	refdb2_C_score_F_mc[refdb] = (m, c)

##############################################################
# Log-linear fits to CDF(prefilter)
##############################################################
searchdb_refdb2prefilter_mc = {}
for searchdb in searchdbs:
	for refdb in refdbs:
		if refdb == "scop40":
			loglinfn = "../P_prefilter/" + searchdb + "_fit.tsv"
		else:
			loglinfn = "../P_prefilter/" + searchdb + "_c_fit.tsv"
		f = open(loglinfn)
		line = f.readline()
		f.close()
		# m=14.68, c=0.008205
		M = re.search(r"m=([0-9.e+-]+).*c=([0-9.e+-]+)", line)
		assert not M is None, "m=, c= not found in edffn=" + loglinfn
		m = float(M.group(1))
		c = float(M.group(2))
		searchdb_refdb2prefilter_mc[ (searchdb, refdb) ] = (m, c)

##############################################################
# C++ reseek_calibrate2.h
##############################################################
fh = open("reseek_calibrate2.h", "w")

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

##############################################################
# E-value calculation from v2.5 for comparison
##############################################################
def calc_evalue_reseekv25(ts, dbsize):
	a = 5.0
	b = -40.0
	logE = a + b*ts
	E_scop = math.exp(logE)/11211
	E = E_scop*dbsize
	return E

##############################################################
# E-value estimation with fitted parameters
##############################################################
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

##############################################################
# E-value table
##############################################################
sys.stderr.write("evalue.tsv\n")
f = open("evalue.tsv", "w")
s = "TS"
for searchdb in searchdbs:
	for refdb in [ "", "c" ]:
		for mode in [ "F", "S" ]:
			s += "\t" + searchdb + refdb + "/" + mode
			if searchdb == "scop40":
				if refdb == "":
					s += "\t" + searchdb + refdb + "/v2.5"
				s += "\t" + searchdb + refdb + "/" + mode + "="
f.write(s + '\n')

def fmtE(E):
	if E > 10:
		return ">10"
	elif E == 0:
		return "0"
	return "%.2e" % E

# Save estimated E-values in dictionary for plotting
edict = {}
for searchdb in searchdbs:
	for refdb in refdbs:
		for mode in modes:
			edict[(searchdb, refdb, mode)] = []

ts_values = []
for binidx in range(0, 21):
	ts = 0.05 + binidx*0.05
	ts_values.append(ts)
	s = "%.2f" % ts
	for searchdb in searchdbs:
		for refdb in refdbs:
			for mode in modes:
				evalue = estimate_evalue(ts, mode, searchdb, refdb)
				edict[(searchdb, refdb, mode)].append(evalue)
				s += "\t%s" % fmtE(evalue)
				if searchdb == "scop40":
					if refdb == "scop40":
						E25 = calc_evalue_reseekv25(ts, 11211)
						s += "\t%s" % fmtE(E25)
					FPEPQ = get_measured_FPEPQ(ts, mode, refdb)
					s += "\t%s" % fmtE(FPEPQ)
	f.write(s + '\n')
f.close()

e25s = []
for binidx in range(0, 21):
	ts = 0.05 + binidx*0.05
	evalue = calc_evalue_reseekv25(ts, 11211)
	e25s.append(evalue)
edict[("scop40", "scop40", "v25")] = e25s

##############################################################
# Table for comparing C_score_F fit to measured on SCOP40
##############################################################
sys.stderr.write("C_score_F.tsv\n")
f = open("C_score_F.tsv", "w")
s = "TS"
s += "\tSCOP40"
s += "\tSCOP40_fit"
s += "\tSCOP40c"
s += "\tSCOP40c_fit"
f.write(s + '\n')

for binidx in range(0, 9):
	ts = 0.05 + binidx*0.05
	s = "%.2f" % ts
	for refdb in [ "scop40", "scop40c" ]:
		C_score_F_measured = get_measured_C_score_F(ts, refdb)
		C_score_F_m, C_score_F_c = get_C_score_F_mc(refdb)
		C_score_F_fit = get_loglin_C_score_F(ts, C_score_F_m, C_score_F_c)
		s += "\t%.3e" % C_score_F_measured
		s += "\t%.3e" % C_score_F_fit
	f.write(s + '\n')
f.close()

##############################################################
# Table for comparing CDF_prefilter fit to measured
##############################################################
sys.stderr.write("CDF_prefilter.tsv\n")
f = open("CDF_prefilter.tsv", "w")
s = "TS"
for searchdb in searchdbs:
	for refdb in [ "", "c" ]:
		s += "\t" + searchdb + refdb
		s += "\t" + searchdb + refdb + "_fit"
f.write(s + '\n')

for binidx in range(0, 21):
	ts = 0.05 + binidx*0.05
	s = "%.2f" % ts
	for searchdb in searchdbs:
		for refdb in refdbs:
			CDF_prefilter_m, CDF_prefilter_c = get_CDF_prefilter_mc(searchdb, refdb)
			CDF_prefilter = get_loglin_CDF_prefilter(ts, CDF_prefilter_m, CDF_prefilter_c)
			CDF_prefilter_measured = get_measured_CDF_prefilter(searchdb, refdb, ts)
			s += "\t%.3g" % CDF_prefilter_measured
			s += "\t%.3g" % CDF_prefilter
	f.write(s + '\n')
f.close()

##############################################################
# Plot figures
##############################################################
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
