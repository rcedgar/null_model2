import math
from fitted_params import *
import dbname2size
from bayes_evalue import *
from foldseek_evalue_calc import *

def pval_Z(z):
	"""One-sided upper-tail p-value for Z score"""
	# standard normal CDF via error function
	p = 0.5 * math.erfc(z / math.sqrt(2))
	return p

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

dbnames = [ "scop40", "afdb50" ]

print("DALI")
s = "Z"
s += "\tE_SCOP40"
s += "\tE_SCOP40Z (Over)"
s += "\tE_AFDB"
s += "\tE_AFDBZ (Over)"
print(s)

m, c = get_m_c("dali", "scop40")
m_c, c_c = get_m_c("dali", "scop40c")
for Z in [ 2, 4, 8, 16, 32 ]:
	s = "%d" % Z
	Pvalue = estimate_C(Z, m, c)
	Pvalue_c = estimate_C(Z, m_c, c_c)
	Pvalue_Z = pval_Z(Z)

	h = estimate_h("dali", "scop40", "scop40")

	dbsize = 11211
	Ec_SCOP40 = estimate_FPEPQ("dali", "scop40c", Z, dbsize, 0.5, h)
	EZ_SCOP40 = Pvalue_Z*dbsize

	dbsize = 214000000
	PF = estimate_PF("dali")
	Ec_AFDB = estimate_FPEPQ("dali", "scop40c", Z, dbsize, 0.5, h)
	EZ_AFDB = Pvalue_Z*dbsize

	s += "\t%.1e" % Ec_SCOP40
	s += "\t%.1e (%.0f)" % (EZ_SCOP40, math.log10(Ec_SCOP40/EZ_SCOP40))

	s += "\t%.1e" % Ec_AFDB
	s += "\t%.1e (%.0f)" % (EZ_AFDB, math.log10(Ec_AFDB/EZ_AFDB))

	print(s)
