import math
import argparse
from bayes_evalue import *

usage = """
Adds estimated E-value according to the log-linear null model to a tab-separated text
(TSV) file with alignment scores.
The first line must have column headings.
The E-value is added as a new column at the end of each line.
"""

AP = argparse.ArgumentParser(description=usage)
AP.add_argument("--input", required=True, help="Input file in TSV format with column names in first line (required)")
AP.add_argument("--output", default="/dev/stdout", help="Output file (default stdout)")
AP.add_argument("--dbsize", required=True, type=int, help="Nr. structures in database (required)")
AP.add_argument("--column", type=int, default=1, help="Column nr. with alignment score (default 1)")
AP.add_argument("--scop40", default=False, action="store_true", help="Calibrate by SCOP40 (default SCOP40c)")
AP.add_argument("--score", required=True, default="E", choices=[ "E", "Z", "TM" ], \
	help="TM, Z (DALI), or E (Foldseek E-value)")
Args = AP.parse_args()

# 0-based column nr.
colnr = Args.column - 1

fin = open(Args.input)
fout = open(Args.output, "w")

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

hdr = fin.readline()[:-1] + "\tE-value_null\n"
fout.write(hdr)

refdb = "scop40c"
if Args.scop40:
	refdb = "scop40"

if Args.score == "TM":
	algo = "tm"
	h = 1
	PF = 1
elif Args.score == "Z":
	algo = "dali"
	h = 0.04
	PF = 0.5
elif Args.score == "E":
	algo = "foldseek"
	h = 0.04
	PF = 0.5
else:
	assert False, "invalid --score " + str(Args.score)

m, c = get_m_c("foldseek", "scop40")
m_c, c_c = get_m_c("foldseek", "scop40c")

def evalue_str(s):
	if Args.score == "E":
		Eprime = 0.05*(s**0.5 + 0.1*s**0.25)
		r = Args.dbsize**0.68
		E = r*Eprime
		if refdb == "scop40":
			E *= 2.5
	else:
		E = estimate_FPEPQ(algo, refdb, s, Args.dbsize, PF, h)
	if E > 10: 
		return ">10"
	return "%.2g" % E

for line in fin:
	line = line[:-1]
	flds = line.split('\t')
	s = float(flds[colnr])
	line += "\t" + evalue_str(s) + "\n"
	fout.write(line)
