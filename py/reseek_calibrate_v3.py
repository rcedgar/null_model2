#!/usr/bin/python3

# reseek_calibrate_v3.py is re-write of reseek_calibrate[_v2].py
#	based on improved formula for E-value with prefilter
#	also add argparse for selecting outputs

import re
import sys
import math
import argparse
import dbname2size
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy import stats
from read_dist import read_dist

####################################################
# ../py/empdist.py 
#	--hits ../big_hits/reseek_verysensitive.scop40.scop40
#	--lookup ../data/scop40.lookup --fields 1,2,5
#	--minscore 0.05 --maxscore 1.05
#	--dbdupes 1 --seed 1 --output 	../edf/reseek_verysensitive_ts.scop40.scop40.scop40
# ../data/scop40.lookup: 11211 doms, 1960 SFs
# 49 excluded doms in hits
# NT 454766, 299066 TP (65.8%), 796898 FP
# q=scop40;qsize=11211;db=scop40;dbsize=11211;
# hits=1095964;tphits=299066;
# maxtps=454766;hitrate=0.00872;
# sens=0.658;prob_f=0.727;
# fphits = hits - tphits = 1095964 - 299066 = 796898
# P(TS >= 0.05) = hits/(11211^2) = 0.00872
# P(FP and TS >= 0.05) = 796898/(11211^2) = 0.0063
####################################################
P_FP_and_TS_ge = 0.0063
####################################################

matplotlib.use('Agg')

AP = argparse.ArgumentParser()
AP.add_argument('--modes', default=["fast", "sensitive"], nargs='+')
AP.add_argument('--searchdbs', default=["scop40", "bfvd", "pdb", "afdb50"], nargs='+')
AP.add_argument('--refdbs', default=["scop40", "scop40c"], nargs='+')
Args = AP.parse_args()

modes = Args.modes
searchdbs = Args.searchdbs
refdbs = Args.refdbs

columns = []
for searchdb in searchdbs:
	for refdb in refdbs:
		for mode in modes:
			columns.append( (mode, searchdb, refdb, "est") )
			if searchdb == "scop40":
				columns.append( (mode, searchdb, refdb, "msd") )
				if mode == "sensitive" and refdb == "scop40":
					columns.append( (mode, searchdb, refdb, "v25") )

###############################################################
# Measured FPEPQ on SCOP40
###############################################################
mode_refdb2FPEPQ_tss = {}
mode_refdb2FPEPQ = {}
for mode in modes:
	for refdb in refdbs:
		edffn = "../edf/reseek_" + mode + "_ts.scop40.scop40." + refdb
		sys.stderr.write(edffn + '\n')
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
		elif refdb == "scop40c":
			cdffn = "../P_prefilter/" + searchdb + "_c_cdf.tsv"
		else:
			assert False, "refdb=" + refdb
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
# C++ reseek_calibrate3.h
##############################################################
fh = open("reseek_calibrate3.h", "w")

for searchdb in searchdbs:
	fh.write("dbsize(%s, %d)\n" % (searchdb, dbname2size.dbname2size[searchdb]))

for refdb in refdbs:
	m, c = refdb2_C_score_F_mc[refdb]
	fh.write("C_score_F_mc(%s, %.3g, %.3g)\n" % (refdb, m, c))

for searchdb in searchdbs:
	for refdb in refdbs:
		m, c = searchdb_refdb2prefilter_mc[ (searchdb, refdb) ]
		fh.write("prefilter_mc(%s, %s, %.3g, %.3g)\n" % \
			(searchdb, refdb, m, c))
		m = None
		c = None
fh.close()

##############################################################
# SCOP40 E-value calculation from v2.5 for comparison
##############################################################
def calc_evalue_reseekv25(ts):
	a = 5.0
	b = -40.0
	logE = a + b*ts
	E_scop40 = math.exp(logE)
	return E_scop40

##############################################################
# E-value estimation with fitted parameters
##############################################################
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

def estimate_pvalue(ts, refdb):
	D = dbname2size.dbname2size[searchdb]
	C_score_F_m, C_score_F_c = get_C_score_F_mc(refdb)
	C_score_F = get_loglin_C_score_F(ts, C_score_F_m, C_score_F_c)
	return min(C_score_F, 1)

def estimate_evalue(ts, mode, searchdb, refdb):
	D = dbname2size.dbname2size[searchdb]
	C_score_F_m, C_score_F_c = get_C_score_F_mc(refdb)
	C_score_F = get_loglin_C_score_F(ts, C_score_F_m, C_score_F_c)
	if mode == "fast":
		CDF_prefilter_m, CDF_prefilter_c = get_CDF_prefilter_mc(searchdb, refdb)
		CDF_prefilter = get_loglin_CDF_prefilter(ts, CDF_prefilter_m, CDF_prefilter_c)
		evalue = D*P_FP_and_TS_ge*CDF_prefilter
	elif mode == "sensitive":
		evalue = D*P_FP_and_TS_ge*C_score_F
	else:
		assert False, "mode=" + mode
	return evalue

##############################################################
# Table for comparing C_score_F fit to measured on SCOP40
##############################################################
sys.stderr.write("C_score_F.tsv\n")
f = open("C_score_F.tsv", "w")
s = "TS"
for refdb in refdbs:
	s += "\t" + refdb
	s += "\t" + refdb + "_fit"
f.write(s + '\n')

for binidx in range(0, 9):
	ts = 0.05 + binidx*0.05
	s = "%.2f" % ts
	for refdb in refdbs:
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
# E-value table
##############################################################

def get_column_value(column, ts):
	mode, searchdb, refdb, method = column
	if method == "v25":
		assert searchdb == "scop40" and refdb == "scop40" and \
			(mode == "fast" or mode == "sensitive")
		return calc_evalue_reseekv25(ts)
	elif method == "msd":
		return get_measured_FPEPQ(ts, mode, refdb)
	elif method == "est":
		return estimate_evalue(ts, mode, searchdb, refdb)
	else:
		assert False, "method=" + method

def fmtE(E):
	if E > 10:
		return ">10"
	elif E == 0:
		return "0"
	return "%.2e" % E

sys.stderr.write("evalue.tsv\n")
f = open("evalue.tsv", "w")

s = "TS"
if "scop40" in refdbs:
	s += "\tP-value"
if "scop40c" in refdbs:
	s += "\tP-value/c"
for column in columns:
	s += "\t" + ".".join(column)
f.write(s + '\n')

for binidx in range(0, 21):
	ts = 0.05 + binidx*0.05
	s = "%.2f" % ts
	if "scop40" in refdbs:
		s += "\t%.2e" % estimate_pvalue(ts, "scop40")
	if "scop40c" in refdbs:
		s += "\t%.2e" % estimate_pvalue(ts, "scop40c")
	for column in columns:
		E = get_column_value(column, ts)
		s += "\t%s" % fmtE(E)
	f.write(s + '\n')
f.close()
