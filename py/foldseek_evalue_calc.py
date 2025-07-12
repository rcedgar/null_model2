import sys
import math
import dbname2size

db2size = {}
db2size["scop40"] = 2e6
db2size["scop40x8"] = 8*2e6
db2size["pdb"] = 200e6
db2size["afdb"] = 15e9
db2size["afdb100k"] = 25e6

def get_size(dbname):
	size = db2size.get(dbname)
	if size is None:
		avglen = 200
		size = dbname2size.dbname2size[dbname]*avglen
	return size

def calc_evalue(pvalue, dbsize):
	return pvalue*dbsize

def calc_evalue_corr(pvalue, dbsize):
	E = pvalue*dbsize
	return E**0.32

def get_pvalue(evalue, dbsize):
	pvalue_dbsize = evalue**3.12
	pvalue = pvalue_dbsize/dbsize
	return pvalue

def convert_evalue(evalue_source, dbsize_source, dbsize_target):
	pvalue = get_pvalue(evalue_source, dbsize_source)
	return calc_evalue_corr(pvalue, dbsize_target)

def convert_evalue2(evalue_source, dbsize_source, dbsize_target):
	pvalue_dbsize = evalue_source**3.1
	pvalue = pvalue_dbsize/dbsize_source
	E = pvalue*dbsize_target
	return E**0.32

def convert_evalue3(evalue_source, dbname_source, dbname_target):
	dbsize_source = get_size(dbname_source)
	dbsize_target = get_size(dbname_target)
	pvalue_dbsize = evalue_source**3.1
	pvalue = pvalue_dbsize/dbsize_source
	E = pvalue*dbsize_target
	return E**0.32

def rce_corrected_evalue(evalue, dbsize):
	Eprime = 0.05*(evalue**0.5 + 0.1*evalue**0.25)
	r = dbsize**0.68
	return r*Eprime

if __name__ == "__main__":
	dbs = [ "scop40", "pdb", "afdb" ]

	s = "%7.7s" % "P-value"
	for db in dbs:
		dbsize = db2size[db]
		s += "  %8.8s" % db
	print(s)

	for pvalue in [ 0.1, 0.01, 0.001, 1e-6, 1e-9 ]:
		s = "%7.1g" % pvalue
		for db in dbs:
			dbsize = db2size[db]
			E = calc_evalue_corr(pvalue, dbsize)
			s += "  %8.3g" % E
		Escop40 = calc_evalue_corr(pvalue, db2size["scop40"])
		Eafdb1 = calc_evalue_corr(pvalue, db2size["afdb"])
		Eafdb2 = convert_evalue(Escop40, db2size["scop40"], db2size["afdb"])
		Eafdb3 = convert_evalue2(Escop40, db2size["scop40"], db2size["afdb"])
	#	s += "     %.3g %.3g" % (Eafdb2, Eafdb3)
		print(s)

	for E, db1, db2 in [ \
			(10, "scop40", "afdb"), \
			(10, "afdb", "scop40"), \
			(8.240E-14, "afdb100k", "afdb"),
			(3.567E-13, "afdb", "afdb100k"),
			(2.948E-13, "scop40", "scop40x8"),
			(5.735E-13, "scop40x8", "scop40"),
			]:
		print("E<%.3g on %s is E<%.3g on %s" % (E, db1, convert_evalue2(E, db2size[db1], db2size[db2]), db2))
