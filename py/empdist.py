#!/usr/bin/python3
import sys
import math
import random
import argparse
import numpy as np
import colnames
import dbname2size

class EmpiricalDistributions:
	def __init__(self, nrbins, fnout):
		self.nrbins = nrbins
		self.comment_lines = []

		self.colnames = colnames.get_colnames()

	def add_comment(self, s):
		self.comment_lines.append(s + '\n')
		sys.stderr.write("# " + s + '\n')

	# Scop family identifier looks like a.1.2.3 
	#     a    1           2      3
	# class.fold.superfamily.family
	def get_sf_from_fam(self, fam):
		flds = fam.split('.')
		assert len(flds) == 4
		sf = flds[0] + "." + flds[1] + '.' + flds[2]
		return sf

	def write_sublookup(self, fn):
		if fn is None:
			return
		with open(fn, "w") as file:
			for dom in self.doms:
				fam = self.dom2fam[dom]
				file.write("%s\t%s\n" % (dom, fam))

	def subsample_scopclass(self, scopclass):
		if scopclass is None:
			return
		classdot = scopclass + '.'
		nr_doms_before = len(self.doms)
		nr_sfs_before = len(self.sfs)
		keep_doms = set()
		keep_sfs = set()
		for dom in self.doms:
			fam = self.dom2fam.get(dom, "")
			if fam.startswith(classdot):
				keep_doms.add(dom)
				sf = self.dom2sf.get(dom)
				keep_sfs.add(sf)
		self.doms = keep_doms
		self.sfs = keep_sfs
		nr_doms_after = len(self.doms)
		nr_sfs_after = len(self.sfs)
		self.set_sf2doms()
		self.add_comment("subsample_scopclass(%c) %d / %d doms, %d / %d SFs\n" \
			% (scopclass, nr_doms_after, nr_doms_before, nr_sfs_after, nr_sfs_before))

	def subsample_nrdoms(self, n):
		if n is None or n == 1:
			return
		assert n > 1
		nr_doms_before = len(self.doms)
		nr_sfs_before = len(self.sfs)
		keep_doms = list(self.doms)
		random.shuffle(keep_doms)
		nrkeep = len(self.doms)//n
		self.doms = set(keep_doms[:nrkeep])
		keep_sfs = set()
		for dom in self.doms:
			sf = self.dom2sf[dom]
			keep_sfs.add(sf)
		self.sfs = keep_sfs
		nr_doms_after = len(self.doms)
		nr_sfs_after = len(self.sfs)
		self.set_sf2doms()
		self.add_comment("subsample_n(%d) %d / %d doms, %d / %d SFs" \
			% (n, nr_doms_after, nr_doms_before, nr_sfs_after, nr_sfs_before))

	def subsample_sf(self, n):
		if n is None or n == 1:
			return
		assert n > 1
		nr_sfs_before = len(self.sfs)
		nr_doms_before = len(self.doms)
		sflist = list(self.sfs)
		random.shuffle(sflist)
		nrkeep = len(sflist)//n
		self.sfs = set(sflist[:nrkeep])
		keep_doms = set()
		for sf in self.sfs:
			for dom in self.sf2doms[sf]:
				keep_doms.add(dom)
		self.doms = keep_doms
		nr_doms_after = len(self.doms)
		nr_sfs_after = len(self.sfs)
		self.set_sf2doms()
		self.add_comment("subsample_sf(%d) %d / %d doms, %d / %d SFs" \
			% (n, nr_doms_after, nr_doms_before, nr_sfs_after, nr_sfs_before))

	def include(self, fn):
		if fn is None:
			return
		nr_sfs_before = len(self.sfs)
		nr_doms_before = len(self.doms)
		self.doms = set( [ line.strip() for line in open(fn) ] )
		self.sfs = set()
		doms_copy = self.doms.copy()
		for dom in doms_copy:
			sf = self.dom2sf.get(dom)
			if sf is None:
				self.doms.remove(dom)
				continue
			self.sfs.add(sf)
		nr_doms_after = len(self.doms)
		nr_sfs_after = len(self.sfs)
		self.set_sf2doms()
		self.add_comment("include(%s) %d / %d doms, %d / %d SFs\n" \
			% (fn, nr_doms_after, nr_doms_before, nr_sfs_after, nr_sfs_before))

	def get_nrdoms(self):
		return len(self.doms)

	def dom_is_singleton(self, dom):
		sf = self.dom2sf[dom]
		return len(self.sf2doms[sf]) == 1

	# number of non-singleton domains, i.e. number of domains
	#  with a possible TP top-hit
	def nr_non_singleton_doms(self):
		ns = 0
		for dom in self.doms:
			sf = self.dom2sf[dom]
			sfsize = len(self.sf2doms[sf])
			if sfsize > 1:
				ns += 1
		return ns

	# nt = number of TPs in all-vs-all excluding self-hits
	def nr_possible_tps_excluding_self_score(self):
		nt = 0
		for sf in list(self.sfs):
			sfdoms = self.sf2doms[sf]
			sfsize = len(sfdoms)
			nt += sfsize*(sfsize - 1)

		try:
			dbdupes = self.dbdupes
		except:
			dbdupes = 1
		nt *= dbdupes
		return nt

	def read_lookup(self, fn):
		self.lookupfn = fn
		self.doms = set()
		self.sfs = set()
		self.dom2fam = {}
		self.dom2sf = {}
		self.sf2doms = {}
		nr_missing_sfs = 0
		for line in open(fn):
			flds = line[:-1].split('\t')
			dom = flds[0]
			assert not dom in self.doms
			self.doms.add(dom)
			fam = flds[1]
			sf = self.get_sf_from_fam(fam)
			self.dom2fam[dom] = fam
			self.dom2sf[dom] = sf
			if not sf in self.sfs:
				self.sfs.add(sf)
				self.sf2doms[sf] = []
			self.sf2doms[sf].append(dom)

		self.nrdoms = len(self.doms)
		self.nrsfs = len(self.sfs)
		self.add_comment("%s: %d doms, %d SFs" \
			% (fn, len(self.doms), len(self.sfs)))

	def get_dom_from_label(self, label):
		label = label.replace(".pdb", "")
		n = label.find('/')
		if n > 0:
			label = label[:n]
		if label.startswith("DUPE"):
			n = label.find('_')
			label = label[n+1:]
		return label

	def set_sf2doms(self):
		new_sfs = set()
		new_sf2doms = {}
		for dom in self.doms:
			sf = self.dom2sf.get(dom)
			if sf is None:
				continue
			if not sf in new_sfs:
				new_sfs.add(sf)
				new_sf2doms[sf] = []
			new_sf2doms[sf].append(dom)
		self.sfs = new_sfs
		self.sf2doms = new_sf2doms

	def read_hits(self, fn, fldnr_q, fldnr_t, fldnr_score):
		############################################
		# per-hit
		############################################
		self.qs = []		# domain label as string
		self.ts = []		# domain label as string
		self.scores = []	# scores
		self.scores_T = []	# TP scores
		self.scores_F = []	# FP scores

		############################################
		# per-dom
		############################################
		self.topscores = []		# top-hit scores
		self.topscores_T = []	# top scores which are TP
		self.topscores_F = []	# top scores which are FP

		self.dom2topscore =	{}
		self.dom2topscore_is_T = {}

		maxfldnr = max(fldnr_q, fldnr_t, fldnr_score)

		self.doms_in_hits = set()
		doms_not_in_lookup = set()
		nr_loscore = 0
		nr_hiscore = 0
		nr_selfhits = 0
		nr_score_not_in_lookup = 0
		nr_score = 0
		linenr = 0
		for line in open(fn):
			if line.startswith('#'):
				continue
			linenr += 1
			flds = line[:-1].split('\t')
			if len(flds) <= maxfldnr:
				sys.stderr.write("Bad line %d: '%s'\n" \
					% (linenr, line[:-1]))
				assert False, "not enough fields"
			q = self.get_dom_from_label(flds[fldnr_q])
			t = self.get_dom_from_label(flds[fldnr_t])
			nr_score += 1
			if nr_score%100000 == 0:
				sys.stderr.write("%.1f M\r" % (nr_score/1e6))
			self.doms_in_hits.add(q)
			self.doms_in_hits.add(t)
			if not q in self.doms or not t in self.doms:
				continue
			if q == t:
				nr_selfhits += 1
				continue

			sfq = self.dom2sf.get(q)
			sft = self.dom2sf.get(t)
			if sfq is None:
				nr_score_not_in_lookup += 1
				doms_not_in_lookup.add(q)
			if sft is None:
				nr_score_not_in_lookup += 1
				doms_not_in_lookup.add(t)
				continue
			is_T = (sfq == sft)

			score = float(flds[fldnr_score])

			if self.evalues:
				if score < self.minevalue:
					nr_loscore += 1
					score = self.minevalue
				elif score > self.maxevalue:
					nr_hiscore += 1
					continue
				score = -math.log10(score)
			else:
				if not self.minscore is None and score < self.minscore:
					nr_loscore += 1
					continue
				if not self.maxscore is None and score > self.maxscore:
					score = self.maxscore
					nr_hiscore += 1
			curr_score = self.dom2topscore.get(q)
			if curr_score is None or score > curr_score:
				self.dom2topscore[q] = score
				self.dom2topscore_is_T[q] = is_T

			self.qs.append(q)
			self.ts.append(t)
			self.scores.append(score)
			try:
				x = self.filtered_hits
			except:
				self.filtered_hits = None
			if not self.filtered_hits is None:
				s = q
				s += "\t" + t
				s += "\t%.6g" % score
				self.filtered_hits.write(s + '\n')
			if is_T:
				self.scores_T.append(score)
			else:
				self.scores_F.append(score)

		sys.stderr.write("%.1f M\n" % (nr_score/1e6))
		s = "%d excluded doms in hits" % len(self.doms_in_hits - self.doms)
		self.add_comment(s)

		nrhits = len(self.qs)
		s = "%d hits" % nrhits
		s += ", %d pegged hi, %d discarded lo" % (nr_hiscore, nr_loscore)
		s += ", %d not in lookup, %d self" % (nr_score_not_in_lookup, nr_selfhits)
		self.add_comment(s)

		nr_tp_score = len(self.scores_T)
		nr_fp_score = len(self.scores_F)
		NQ = len(self.doms)
		NT = self.nr_possible_tps_excluding_self_score()
		s = "NT %d" % NT
		s += ", %d TP (%.1f%%)" % (nr_tp_score, (nr_tp_score*100)/NT)
		s += ", %d FP" % nr_fp_score
		self.add_comment(s)

		if self.minscore is None:
			self.minscore = min(self.scores)
		if self.maxscore is None:
			self.maxscore = max(self.scores)

		for dom in self.doms:
			if self.dom_is_singleton(dom):
				continue
			topscore = self.dom2topscore.get(dom)
			if topscore is None:
				continue
			topscore_is_T = self.dom2topscore_is_T[dom]
			self.topscores.append(topscore)
			if topscore_is_T:
				self.topscores_T.append(topscore)
			else:
				self.topscores_F.append(topscore)

		self.scores = np.array(self.scores, dtype=np.float32)
		self.scores_T = np.array(self.scores_T, dtype=np.float32)
		self.scores_F = np.array(self.scores_F, dtype=np.float32)
		self.topscores = np.array(self.topscores, dtype=np.float32)
		self.topscores_T = np.array(self.topscores_T, dtype=np.float32)
		self.topscores_F = np.array(self.topscores_F,dtype=np.float32)

	def make_bins(self):
		try:
			ib = self.integer_bins
		except:
			ib = False
		if ib:
			self.minscore = math.floor(self.minscore)
			self.maxscore = math.ceil(self.minscore)
			r = self.maxscore - self.minscore + 1
			dx = (self.maxscore - self.minscore + 1)/self.nrbins
			dxi = math.ceil(dx)
			n = math.ceil(r/dxi)
			print(f"{r=} {dx=} {dxi=} {n=} {self.nrbins=}")
			assert False
			self.binmids = np.linspace(self.minscore, self.maxscore, self.nrbins)
			self.binedges = np.linspace(self.minscore, self.maxscore, self.nrbins+1)
		else:
			self.binmids = np.linspace(self.minscore, self.maxscore, self.nrbins)
			self.binedges = np.linspace(self.minscore, self.maxscore, self.nrbins+1)

	def make_NP(self, name):
		values = eval("self." + name)
		n = len(values)
		total = sum(values)
		N_value, _ = np.histogram(values, self.binedges)
		P_value = N_value/n
		sum_probs = np.sum(P_value)
		if sum_probs < 0.99 or sum_probs > 1.01:
			w = "name=%s n=%d sum_probs=%.3g" % (name, n, sum_probs)
			self.add_comment(w)
			sys.stderr.write("WARNING " + w + '\n')
		return N_value, P_value

	def get_reverse_CDF(self, nameP):
		P = self.get_vec(nameP)
		sum_probs = np.sum(P)
		if sum_probs < 0.99 or sum_probs > 1.01:
			w = "name=%s n=%d sum_probs=%.3g" % (nameP, len(P), sum_probs)
			self.add_comment(w)
			sys.stderr.write("WARNING " + w + '\n')
		return np.cumsum(P[::-1])[::-1]

	def precision(self, tps, ns):
		prec = []
		for binidx in range(self.nrbins):
			tp = tps[binidx]
			n = ns[binidx]
			assert tp <= n
			if n == 0:
				prec.append(0)
			else:
				prec.append(tp/n)
		return np.array(prec, dtype=np.float32)

	def accumN(self, ns):
		return np.cumsum(ns[::-1])[::-1]

	def make_NPCs(self):
		self.N_score, self.P_score = self.make_NP("scores")
		self.N_score_T, self.P_score_T = self.make_NP("scores_T")
		self.N_score_F, self.P_score_F = self.make_NP("scores_F")
		assert np.array_equal(self.N_score_T + self.N_score_F, self.N_score)

		self.M_score = self.accumN(self.N_score)
		self.M_score_T = self.accumN(self.N_score_T)
		self.M_score_F = self.accumN(self.N_score_F)

		self.N_topscore, self.P_topscore = self.make_NP("topscores")
		self.N_topscore_T, self.P_topscore_T = self.make_NP("topscores_T")
		self.N_topscore_F, self.P_topscore_F = self.make_NP("topscores_F")
		assert np.array_equal(self.N_topscore_T + self.N_topscore_F, self.N_topscore)

		self.M_topscore = self.accumN(self.N_topscore)
		self.M_topscore_T = self.accumN(self.N_topscore_T)
		self.M_topscore_F = self.accumN(self.N_topscore_F)

		self.P_T_score = self.precision(self.N_score_T, self.N_score)
		self.P_F_score = self.precision(self.N_score_F, self.N_score)

		self.C_T_score = self.precision(self.M_score_T, self.M_score)
		self.C_F_score = self.precision(self.M_score_F, self.M_score)

		self.P_T_topscore = self.precision(self.N_topscore_T, self.N_topscore)
		self.P_F_topscore = self.precision(self.N_topscore_F, self.N_topscore)

		self.C_T_topscore = self.precision(self.M_topscore_T, self.M_topscore)
		self.C_F_topscore = self.precision(self.M_topscore_F, self.M_topscore)

		self.C_score = self.get_reverse_CDF("P_score")
		self.C_topscore = self.get_reverse_CDF("P_topscore")

		self.C_score_T = self.get_reverse_CDF("P_score_T")
		self.C_score_F = self.get_reverse_CDF("P_score_F")

		self.C_topscore_T = self.get_reverse_CDF("P_topscore_T")
		self.C_topscore_F = self.get_reverse_CDF("P_topscore_F")

	def calc_cate(self):
		ns = self.nr_non_singleton_doms()
		self.cate_sens = self.M_topscore_T/ns
		self.cate_epq = self.M_topscore_F/ns

	def calc_cve(self):
		NT = self.nr_possible_tps_excluding_self_score()
		NQ = len(self.doms)

		self.cve_sens = np.cumsum(self.N_score_T[::-1])[::-1]/NT
		self.cve_epq = np.cumsum(self.N_score_F[::-1])[::-1]/NQ

	def get_colvalue(self, name, binidx):
		vec = self.get_vec(name)
		return vec[binidx]

	def get_vec(self, name):
		return eval("self." + name)

	def assert_good_P(self, colname):
		P = self.get_vec(colname)
		sum_probs = sum(P)
		if sum_probs < 0.99 or sum_probs > 1.01:
			w = "name=%s n=%d sum_probs=%.3g" % (colname, len(P), sum_probs)
			self.add_comment(w)
			sys.stderr.write("WARNING " + w + '\n')

	def assert_good_C(self, colname):
		C = self.get_vec(colname)
		P = C[0]
		if P < 0.99 or P > 1.01:
			w = "name=%s C[0]=%.3g" % (colname, P)
			self.add_comment(w)
			sys.stderr.write("WARNING " + w + '\n')

	def assert_sum_to_one(self, name_P1, name_P2):
		P1 = self.get_vec(name_P1)
		P2 = self.get_vec(name_P2)
		nr = 0
		nr1 = 0
		for binidx in range(self.nrbins):
			p1 = P1[binidx]
			p2 = P2[binidx]
			if p1 == 0 and p2 == 0:
				continue
			sum12 = p1 + p2
			nr += 1
			if sum12 > 0.99 and sum12 < 1.01:
				nr1 += 1
		if nr1 < 0.9*nr:
		   sys.stderr.write("assert_sum_to_one(%s, %s, %d, %d)\n" % (name_P1, name_P2, nr1, nr))

	def assert_probs(self):
		for colname in self.colnames:
			if colname.startswith("P_score") or colname.startswith("P_topscore"):
				self.assert_good_P(colname)
			if colname.startswith("C_score") or colname.startswith("C_topscore"):
				self.assert_good_C(colname)
		self.ones = np.ones((self.nrbins, ))
		self.assert_sum_to_one("P_T_score", "P_F_score")
		self.assert_sum_to_one("P_T_topscore", "P_F_topscore")
		sys.stderr.write("probs ok\n")

	def totsv(self, fn):
		if fn is None:
			return
		file = open(fn, 'w')
		s = '\t'.join(self.colnames)
		if Args.evalues:
			s += "\tE-value"
		file.write(s + '\n')
		for binidx in range(self.nrbins):
			s = ""
			for colname in self.colnames:
				value = self.get_colvalue(colname, binidx)
				if s != "":
					s += "\t"
				s += "%.4g" % value
			if Args.evalues:
				score = self.binmids[binidx]
				evalue = 10**(-score)
				s += "\t%.4g" % evalue
			file.write(s + '\n')

		qsize = dbname2size.dbname2size.get(self.qname)
		if qsize is None:
			assert False, "dbname2size(%s)" % self.qname
		try:
			dbdupes = self.dbdupes
		except:
			dbdupes = 1
		dbsize = len(self.doms)*dbdupes
		nrhits = sum(self.N_score)
		nrtphits = sum(self.N_score_T)
		nrfphits = sum(self.N_score_F)
		assert nrtphits + nrfphits == nrhits
		maxtps = self.nr_possible_tps_excluding_self_score()
		prob_f = nrfphits/nrhits
		prob_f_and_score_ge_minscore = nrfphits/(dbsize*dbsize)
		sens = nrtphits/maxtps

		if self.subsf != 1 or self.subn != 1:
			qsize = dbsize

		lookupfn = Args.lookup
		ref = lookupfn.split('/')[-1].split('.')[0]

		s = "" # don't use '# ', add_comment() does this
		s += "q=%s;" % self.qname
		s += "qsize=%d;" % qsize
		s += "db=%s;" % self.dbname
		s += "dbsize=%d;" % dbsize
		s += "ref=%s;" % ref
		if dbdupes > 1:
			s += "dbdupes=%d;" % dbdupes
		if self.subsf > 1:
			s += "subsf=%d;" % self.subsf
		if self.subn > 1:
			s += "subsf=%d;" % self.subn
		s += "hits=%d;" % nrhits
		s += "tphits=%d;" % nrtphits
		s += "fphits=%d;" % nrfphits
		s += "maxtps=%d;" % maxtps
		s += "hitrate=%.3g;" % (nrhits/(dbsize*qsize))
		s += "fphitrate=%.3g;" % (nrhits/(dbsize*qsize))
		s += "sens=%.3g;" % sens
		s += "prob_f=%.3g;" % prob_f
		s += "prob_fge=%.3g;" % prob_f_and_score_ge_minscore
		self.add_comment(s)

		file.write("# " + " ".join(sys.argv) + "\n")
		for line in self.comment_lines:
			file.write("# " + line)
		file.close()

		sys.stderr.write('='*len(fn) + '\n')
		sys.stderr.write(fn + '\n')
		sys.stderr.write('='*len(fn) + '\n')

if __name__ == "__main__":
	sys.stderr.write(' ' .join(sys.argv) + '\n')
	AP = argparse.ArgumentParser()
	AP.add_argument("--hits", required=True, help="Hits tsv")
	AP.add_argument("--fields", required=False, default="1,2,3", help="query,target,score field numbers (default 1,2,3)")
	AP.add_argument("--include", required=False, help="Text file with domains to include, one per line (default include all)")
	AP.add_argument("--lookup", required=False, type=str, default="../data/scop40.lookup", 
				 help="Tsv with 1. domain 2. scopid e.g. a.1.2.3, default ../data/scop40.lookup")
	AP.add_argument("--output", required=False, type=str, default="/dev/stdout", help="Output file, default stdout")
	AP.add_argument("--nrbins", required=False, type=int, default="100", help="Nr. bins, default 100")
	AP.add_argument("--seed", required=False, type=int, default=1, help="Random seed, default 1")
	AP.add_argument("--subn", required=False, type=int, default=1, help="Subsample 1/subn domains, default 1")
	AP.add_argument("--subsf", required=False, type=int, default=1, help="Subsample 1/subsf SFs, default 1")
	AP.add_argument("--sublookup", required=False, type=str, help="Output lookup file for subn or subsf")
	AP.add_argument("--integer_bins", required=False, default=False, action="store_true", help="Integer bin boundaries")
	AP.add_argument("--evalues", required=False, default=False, action="store_true", help="E-values, use score = -log10(score_field)")
	AP.add_argument("--minevalue", required=False, type=float, default=1e-20, help="Min E-value for binning, peg if lower, default 1e-20")
	AP.add_argument("--maxevalue", required=False, type=float, default=10, help="Max E-value for binning, discard if higher, default 10")
	AP.add_argument("--minscore", required=False, type=float, help="Min score for binning (discard if lower)")
	AP.add_argument("--maxscore", required=False, type=float, help="Max score for binning (peg if higher)")
	AP.add_argument("--scopclass", required=False, type=str, choices = [ "a", "b", "c", "d" ], help="Only this SCOP class, default all")
	AP.add_argument("--dbdupes", required=False, type=int, default=1, help="nr. DUPEs in db")
	AP.add_argument("--filtered_hits", required=False, type=str) # for trouble-shooting
	AP.add_argument("--dbname")
	AP.add_argument("--qname")

	Args = AP.parse_args()
	random.seed(Args.seed)

	if not Args.dbname is None and not Args.qname is None:
		qname = Args.qname
		dbname = Args.dbname
	else:
		qname, dbname = dbname2size.get_names(Args.hits, Args.lookup)

	if Args.evalues:
		assert not Args.minevalue is None
		assert not Args.maxevalue is None
		assert Args.minscore is None
		assert Args.maxscore is None
		Args.minscore = -math.log10(Args.maxevalue)
		Args.maxscore = -math.log10(Args.minevalue)
	else:
		assert not Args.minscore is None
		assert not Args.maxscore is None

	sys.stderr.write("hits %s\n" % Args.hits)
	if Args.evalues:
		sys.stderr.write("evalues %.3g  ..  %.3g (%.3g .. %.3g)\n" % \
			(Args.minevalue, Args.maxevalue, Args.minscore, Args.maxscore))
	else:
		sys.stderr.write("scores %.3g  ..  %.3g\n" % (Args.minscore, Args.maxscore))

	fs = Args.fields.split(",")
	if len(fs) != 3:
		 assert False, "--fields must be 3 comma-separated 1-based field numbers"

	qfldnr = int(fs[0]) - 1
	tfldnr = int(fs[1]) - 1
	scorefldnr = int(fs[2]) - 1

	filtered_hits = None
	if not Args.filtered_hits is None:
		filtered_hits = open(Args.filtered_hits, "w")

	ED = EmpiricalDistributions(Args.nrbins, Args.output)
	ED.subsf = Args.subsf
	ED.subn = Args.subn
	ED.filtered_hits = filtered_hits
	ED.qname = qname
	ED.dbname = dbname
	ED.dbdupes = Args.dbdupes
	ED.minscore = Args.minscore
	ED.maxscore = Args.maxscore
	ED.minevalue = Args.minevalue
	ED.maxevalue = Args.maxevalue
	ED.evalues = Args.evalues
	ED.searchdbname = Args.dbname
	ED.read_lookup(Args.lookup)
	ED.include(Args.include)
	ED.subsample_sf(Args.subsf)
	ED.subsample_nrdoms(Args.subn)
	ED.subsample_scopclass(Args.scopclass)
	ED.write_sublookup(Args.sublookup)
	ED.read_hits(Args.hits, qfldnr, tfldnr, scorefldnr)
	ED.make_bins()
	ED.make_NPCs()
	ED.calc_cve()
	ED.calc_cate()
	ED.assert_probs()
	ED.totsv(Args.output)
	if not filtered_hits is None:
		filtered_hits.close()
