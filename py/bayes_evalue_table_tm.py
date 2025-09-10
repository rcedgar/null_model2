import math
from fitted_params import *
import dbname2size
from bayes_evalue import *
from foldseek_evalue_calc import *

def TM_pvalue_xu_yang(TM):
	mu = location = 0.152
	beta = scale = 0.0242
	ratio = (TM - mu)/beta
	p = 1 - math.exp(-math.exp(-ratio))
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

def hdr(score_name):
	s = score_name
	s += "\tE_SCOP40c"
	s += "\tE_SCOP40x"
	s += " (Over)"
	s += "\tE_AFDBc"
	s += "\t%E_AFDBx"
	s += "  (Over)"
	print(s)

m, c = get_m_c("tm", "scop40")
m_c, c_c = get_m_c("tm", "scop40c")
print("\nTM-align")
hdr("TM")
for i in range(5):
	TM = 0.5 + i/10
	s = "%.2f" % TM
	Px = TM_pvalue_xu_yang(TM)
	Pvalue_c = estimate_C(TM, m_c, c_c)

	Evalue_SCOP40_c = 11211*Pvalue_c
	Evalue_SCOP40_x = 11211*Px

	Evalue_ADFB_c = 214000000*Pvalue_c
	Evalue_ADFB_x = 214000000*Px

	s += "\t%.1e" % Evalue_SCOP40_c
	s += " \t%.1e" % Evalue_SCOP40_x
	s += " (%.0f)" % math.log10(Evalue_SCOP40_c/Evalue_SCOP40_x)

	s += "\t%.1e" % (Evalue_ADFB_c)
	s += "\t%.1e" % (Evalue_ADFB_x)
	s += " (%.0f)" % math.log10(Evalue_ADFB_c/Evalue_ADFB_x)
	print(s)
