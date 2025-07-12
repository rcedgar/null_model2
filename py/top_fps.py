#!/usr/bin/python3

import sys
import math
import argparse
import numpy as np

AP = argparse.ArgumentParser()
AP.add_argument("--hits", required=True, help="Hits tsv")
AP.add_argument("--edf", required=True, help="P_T_score")
AP.add_argument("--minprob", required=False, type=float, default=0.5)
AP.add_argument("--lookup", required=False, type=str, default="../data/scop40.lookup", 
				help="Tsv with 1. domain 2. scopid e.g. a.1.2.3, default ../data/scop40.lookup")
AP.add_argument("--fields", required=False, default="1,2,3", help="query,target,score field numbers (default 1,2,3)")
AP.add_argument("--output", required=False, type=str, default="/dev/stdout", help="Output TSV")
AP.add_argument("--evalues", default=False, action="store_true")
Args = AP.parse_args()

fs = Args.fields.split(",")
if len(fs) != 3:
		assert False, "--fields must be 3 comma-separated 1-based field numbers"

fout = open(Args.output, "w")

qfldnr = int(fs[0]) - 1
tfldnr = int(fs[1]) - 1
scorefldnr = int(fs[2]) - 1

def read_dist(fn, distname):
	bin_mids = []
	fld_nr = None
	v = []
	for line in open(fn):
		if line.startswith('#'):
			continue
		if fld_nr is None:
			hdr = line[:-1].split('\t')
			assert hdr[0] == "binmids"
			for i in range(len(hdr)):
				if hdr[i] == distname:
					fld_nr = i
					break
			if fld_nr is None:
				assert False, "distname=%s not found in fn=%s" % (distname, fn)
			continue
		if len(line.strip()) == 0:
			continue
		flds = line[:-1].split('\t')
		bin_mid = float(flds[0])
		x = float(flds[fld_nr])

		bin_mids.append(bin_mid)
		v.append(x)

	return bin_mids, np.array(v, dtype=np.float32)

def get_sf_from_fam(fam):
	flds = fam.split('.')
	assert len(flds) == 4
	sf = flds[0] + "." + flds[1] + '.' + flds[2]
	return sf

sfs = set()
dom2sf = {}
for line in open(Args.lookup):
	flds = line[:-1].split('\t')
	dom = flds[0]
	fam = flds[1]
	sf = get_sf_from_fam(fam)
	dom2sf[dom] = sf

bin_mids, P_T_score = read_dist(Args.edf, "P_T_score")
bin_mids = np.array(bin_mids, dtype=np.float32)

def get_P_T(score):
	return np.interp(score, bin_mids, P_T_score)

def get_dom_from_label(label):
	label = label.replace(".pdb", "")
	n = label.find('/')
	if n > 0:
		label = label[:n]
	if label.startswith("DUPE"):
		n = label.find('_')
		label = label[n+1:]
	return label

n = 0
for line in open(Args.hits):
	flds = line[:-1].split('\t')
	score = float(flds[scorefldnr])
	if Args.evalues:
		evalue = score
		if evalue < 1e-20:
			evalue = 1e-20
		score = -math.log10(evalue)
	q = get_dom_from_label(flds[qfldnr])
	t = get_dom_from_label(flds[tfldnr])
	if q == t:
		continue
	qsf = dom2sf.get(q)
	tsf = dom2sf.get(t)
	if qsf is None or tsf is None:
		continue
	if qsf == tsf:
		continue
	P = get_P_T(score)
	if P < Args.minprob:
		continue
	# if q == "d3d9ya_" and t == "d1j3wa_":
	# 	print(score, P, line)
	s = "%.4g" % P
	s += "\t" + q + "/" + str(qsf)
	s += "\t" + t + "/" + str(tsf)
	fout.write(s + '\n')
	n += 1
fout.close()
sys.stderr.write("%d %s\n" % (n, Args.hits))
