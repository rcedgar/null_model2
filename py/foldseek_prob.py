#!/usr/bin/python3

import sys
import os
import math
import statistics
from bayes_evalue import *
from dbname2size import dbname2size

hitsfn = "../big_hits/foldseek_exhaustive.scop40.scop40"
tsvfn = "../foldseek_prob/annotated_hits.tsv"
summaryfn = "../foldseek_prob/summary.tsv"

NQ = 11211

try:
	os.mkdir("../foldseek_prob")
except FileExistsError:
	pass

ftsv = open(tsvfn, "w")
fsummary = open(summaryfn, "w")

def get_sf_from_fam(fam):
	flds = fam.split('.')
	assert len(flds) == 4
	sf = flds[0] + "." + flds[1] + '.' + flds[2]
	return sf

doms = set()
sfs = set()
dom2fam = {}
dom2sf = {}
sf2doms = {}
nr_missing_sfs = 0
for line in open("../data/scop40.lookup"):
	flds = line[:-1].split('\t')
	dom = flds[0]
	assert not dom in doms
	doms.add(dom)
	fam = flds[1]
	sf = get_sf_from_fam(fam)
	dom2fam[dom] = fam
	dom2sf[dom] = sf
	if not sf in sfs:
		sfs.add(sf)
		sf2doms[sf] = []
	sf2doms[sf].append(dom)

probs = [ "0.999", "0.949", "0.900" ]
float_probs = [ float(prob) for prob in probs ]

prob2nt = {}
prob2nf = {}
prob2ntg = {}
prob2nfg = {}
prob2evalues = {}
for prob in probs:
	prob2nt[prob] = 0
	prob2nf[prob] = 0
	prob2ntg[prob] = 0
	prob2nfg[prob] = 0
	prob2evalues[prob] = []

s = "query"
s += "\ttarget"
s += "\tevalue"
s += "\tprob"
s += "\tTP/FP(SF)"
ftsv.write(s + '\n')
for line in open(hitsfn):
	flds = line[:-1].split('\t')
	assert len(flds) == 5
	q = flds[0]
	t = flds[1]
	if q == t:
		continue
	qsf = dom2sf.get(q)
	tsf = dom2sf.get(t)
	if qsf is None or tsf is None:
		continue
	evalue = float(flds[2])
	bits = float(flds[3])
	prob = flds[4]
	if prob in probs:
		prob2evalues[prob].append(evalue)
		if qsf == tsf:
			prob2nt[prob] += 1
			for prob2 in probs:
				if float(prob2) >= float(prob):
					prob2ntg[prob] += 1
			XP = "TP"
		else:
			prob2nf[prob] += 1
			for prob2 in probs:
				if float(prob2) >= float(prob):
					prob2nfg[prob] += 1
			XP = "FP"
		s = q + "/" + qsf
		s += "\t" + t + "/" + tsf
		s += "\t%.3g" % evalue
		s += "\t" + prob
		s += "\t" + XP
		ftsv.write(s + '\n')

s = "prob"
s += "\tP(T|prob)"
s += "\tE"
s += "\tFPEPQ"
s += "\tEfit_SCOP40"
s += "\tEfit_AFDB50"
fsummary.write(s + '\n')
for prob in probs:
	evalue = statistics.median(prob2evalues[prob])
	score = -math.log10(evalue)
	nt = prob2nt[prob]
	nf = prob2nf[prob]
	FPEPQ = prob2nfg[prob]/NQ
	PT = nt/(nt + nf)

	h = estimate_h("reseek", "scop40", "afdb50")
	dbsize_scop40 = dbname2size["scop40"]
	dbsize_afdb50 = dbname2size["afdb50"]
	PF = estimate_PF("foldseek")
	E_SCOP40 = estimate_FPEPQ("foldseek", "scop40", score, dbsize_scop40, PF, h)
	E_AFDB = estimate_FPEPQ("foldseek", "scop40", score, dbsize_afdb50, PF, h)

	s = prob
	s += "\t%.3f" % PT
	s += "\t%.2g" % evalue
	s += "\t%.2g" % FPEPQ
	s += "\t%.2g" % E_SCOP40
	if E_AFDB > 10:
		s += "\t>10"
	else:
		s += "\t%.2g" % E_AFDB
	fsummary.write(s + '\n')

ftsv.close()
fsummary.close()
