import sys
import os
import re

fout = sys.stdout

def get_edffn(algo, q, db, ref):
	return "../edf/" + algo + "." + q + "." + db + "." + ref

def get_hitrate(edffn):
	hitrate = None
	for line in open(edffn):
		if not line.startswith("#"):
			continue
		if line.find("hitrate=") > 0:
			M = re.search(r"hitrate=([0-9.e]+);", line)
			hitrate = float(M.group(1))
	assert not hitrate is None
	return hitrate

fout.write("\n")
fout.write("algo_q_db2hitrate = {}\n")

def do_hitrate(algo, q, db, ref):
	edffn = get_edffn(algo, q, db, ref)
	hitrate = get_hitrate(edffn)
	algo_ = algo.split('_')[0]
	s = "algo_q_db2hitrate[ ('%s', '%s', '%s') ] = %.3g" % (algo_, q, db, hitrate)
	fout.write(s + '\n')

do_hitrate("dali", "scop40", "scop40", "scop40")
do_hitrate("tm", "scop40", "scop40", "scop40")

do_hitrate("reseek_sensitive_ts", "scop40", "scop40", "scop40")
do_hitrate("reseek_sensitive_ts", "scop40", "bfvd", "none")
do_hitrate("reseek_sensitive_ts", "scop40", "pdb", "none")

do_hitrate("foldseek_exhaustive", "scop40", "scop40", "scop40")
do_hitrate("foldseek_exhaustive", "scop40", "bfvd", "none")
do_hitrate("foldseek_exhaustive", "scop40", "pdb", "none")

####################################################################
# TODO
####################################################################
# do_hitrate("reseek_sensitive_evalue", "scop40", "afpdb50", "none")
# do_hitrate("foldseek_exhaustive", "scop40", "afpdb50", "none")

fout.write("\n")
fout.write("algo_refdb2m_c = {}\n")

algos = [ "tm", "dali", "reseek", "foldseek" ]
refdbs = [ "scop40", "scop40c" ]
for algo in algos:
	for refdb in refdbs:
		algo_ = algo
		if algo == "reseek":
			algo_ = "reseek_ts"
		ar = algo_ + "." + refdb

		f = open("../fit_loglin/" + ar + ".tsv")
		line = f.readline()
		f.close()
		M = re.search(r"m=(.+), c=(.+)", line)
		m = float(M.group(1))
		c = float(M.group(2))
		algo_ = algo.split('_')[0]
		fout.write("algo_refdb2m_c[ ('%s', '%s') ] = (%.4g, %.4g)\n" % (algo_, refdb, m, c))
fout.close()
