import math
from fitted_params import *
import dbname2size
from bayes_evalue import *
from foldseek_evalue_calc import *

def fmt(E, Ec):
	if E > 10: 
		s = "  %7.7s" % ">10"
	else:
		s = "  %7.2g" % E
	if Ec > 10: 
		s += "  %7.7s" % ">10"
	else:
		s += "  %7.2g" % Ec
	return s

dbnames = [ "scop40", "pdb", "afdb50" ]

def hdr(score_name):
	s = "%7.7s" % score_name
	s += "  %7.7s" % "Pval"
	s += "  %7.7s" % "Pvalc"
	for dbname in dbnames:
		s += "  %7.7s" % dbname.upper()
		s += "  %6.6sc" % dbname.upper()
	print(s)

m, c = get_m_c("dali", "scop40")
m_c, c_c = get_m_c("dali", "scop40c")
print("DALI")
hdr("Z-score")
for score in range(5, 65, 5):
	s = "%7d" % score
	Pvalue = estimate_C(score, m, c)
	Pvalue_c = estimate_C(score, m_c, c_c)
	s += "  %7.2g" % Pvalue
	s += "  %7.2g" % Pvalue_c
	for dbname in dbnames:
		h = estimate_h("dali", "scop40", dbname)
		dbsize = dbname2size.dbname2size[dbname]
		PF = estimate_PF("dali")
		E = estimate_FPEPQ("dali", "scop40", score, dbsize, PF, h)
		Ec = estimate_FPEPQ("dali", "scop40c", score, dbsize, PF, h)
		s += fmt(E, Ec)
	print(s)

m, c = get_m_c("tm", "scop40")
m_c, c_c = get_m_c("tm", "scop40c")
print("\nTM-align")
hdr("TM")
for i in range(10):
	score = 0.5 + i/20
	s = "%7.2f" % score
	Pvalue = estimate_C(score, m, c)
	Pvalue_c = estimate_C(score, m_c, c_c)
	s += "  %7.2g" % Pvalue
	s += "  %7.2g" % Pvalue_c
	for dbname in dbnames:
		h = estimate_h("tm", "scop40", dbname)
		dbsize = dbname2size.dbname2size[dbname]
		PF = estimate_PF("tm")
		E = estimate_FPEPQ("tm", "scop40", score, dbsize, PF, h)
		Ec = estimate_FPEPQ("tm", "scop40c", score, dbsize, PF, h)
		s += fmt(E, Ec)
	print(s)

m, c = get_m_c("foldseek", "scop40")
m_c, c_c = get_m_c("foldseek", "scop40c")
print("\nFoldseek")
hdr("E-value")
for score in range(-1, 11):
	evalue = 10**-score
	s = "%7.2g" % evalue
	Pvalue = estimate_C(score, m, c)
	Pvalue_c = estimate_C(score, m_c, c_c)
	s += "  %7.2g" % Pvalue
	s += "  %7.2g" % Pvalue_c
	for dbname in dbnames:
		dbsize = dbname2size.dbname2size[dbname]
		# E = estimate_FPEPQ("foldseek", "scop40", score, dbsize, PF, h)
		# Ec = estimate_FPEPQ("foldseek", "scop40c", score, dbsize, PF, h)
		E = rce_corrected_evalue(evalue, dbsize)
		Ec = rce_corrected_evalue(evalue, dbsize)*Pvalue_c/Pvalue
		s += fmt(E, Ec)
	print(s)

m, c = get_m_c("reseek", "scop40")
m_c, c_c = get_m_c("reseek", "scop40c")
print("\nReseek")
hdr("TS")
for idx in range(15):
	score = idx*0.05
	s = "%7.2f" % score
	Pvalue = estimate_C(score, m, c)
	Pvalue_c = estimate_C(score, m_c, c_c)
	s += "  %7.2g" % Pvalue
	s += "  %7.2g" % Pvalue_c
	for dbname in dbnames:
		h = estimate_h("reseek", "scop40", dbname)
		dbsize = dbname2size.dbname2size[dbname]
		PF = estimate_PF("reseek")
		E = estimate_FPEPQ("reseek", "scop40", score, dbsize, PF, h)
		Ec = estimate_FPEPQ("reseek", "scop40c", score, dbsize, PF, h)
		s += fmt(E, Ec)
	print(s)
