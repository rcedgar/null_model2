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

dbnames = [ "scop40", "afdb50" ]

# s = "%7.7s" % score_name
# s += "  %7.7s" % "Pval"
# s += "  %7.7s" % "Pvalc"
# for dbname in dbnames:
# 	s += "  %7.7s" % dbname.upper()
# 	s += "  %6.6sc" % dbname.upper()
# print(s)

m, c = get_m_c("foldseek", "scop40")
m_c, c_c = get_m_c("foldseek", "scop40c")
print("\nFoldseek")

for score in [ 2, 4, 8, 16 ]:
	E_fs = 10**-score
	s = "%.1e" % E_fs
	Pvalue = estimate_C(score, m, c)
	Pvalue_c = estimate_C(score, m_c, c_c)
	dbname = "scop40"
	dbsize = 11211
	E = rce_corrected_evalue(E_fs, dbsize)
	Ec_SCOP40 = rce_corrected_evalue(E_fs, dbsize)*Pvalue_c/Pvalue
	s += "\t%.1e" % Ec_SCOP40
	s += " (%.0f)" % math.log10(Ec_SCOP40/E_fs)

	dbname = "afdb"
	dbsize = 214e6
	E = rce_corrected_evalue(E_fs, dbsize)
	Ec_AFDB = rce_corrected_evalue(E_fs, dbsize)*Pvalue_c/Pvalue
	s += "\t%.1e" % Ec_AFDB
	s += " (%.0f)" % math.log10(Ec_AFDB/E_fs)

	print(s)
