special_cases = { \
	"binmids" : "score",
	"cve_sens" : "Sensitivity", \
	"cve_epq" : "FPEPQ", \
	"cate_sens" : "Category coverage", \
	"cate_epq" : "Category EPQ" \
	}

names = []

def addname(name):
	assert not name in names
	names.append(name)

addname("binmids")
addname("N_score")
addname("N_score_T")
addname("N_score_F")
addname("N_topscore")
addname("N_topscore_T")
addname("N_topscore_F")
addname("M_score")
addname("M_score_T")
addname("M_score_F")
addname("M_topscore")
addname("M_topscore_T")
addname("M_topscore_F")
addname("P_score")
addname("P_score_T")
addname("P_score_F")
addname("P_T_score")
addname("P_F_score")
addname("P_T_topscore")
addname("P_F_topscore")
addname("C_T_topscore")
addname("C_F_topscore")
addname("C_score")
addname("C_score_T")
addname("C_score_F")
addname("P_topscore")
addname("P_topscore_T")
addname("P_topscore_F")
addname("C_topscore")
addname("C_topscore_T")
addname("C_topscore_F")
addname("C_T_score")
addname("C_F_score")
addname("cve_sens")
addname("cve_epq")
addname("cate_sens")
addname("cate_epq")

def is_name(name):
	return name in names

def get_label(distname):
	label = special_cases.get(distname)
	if not label is None:
		return label

	label = distname
	label = label.replace('_', '(', 1)
	label = label.replace('_', '|', 1)
	label = label.replace('_', ')', 1)
	label = label.replace("C(", "CDF(", 1)
	label += ')'
	return label

label2distname = {}
for distname in names:
	label = get_label(distname)
	label2distname[label] = distname

def get_colnames():
	return names

def get_distname(label):
	return label2distname.get(label)

if __name__ == "__main__":
	names = get_colnames()
	n = max([ len(name) for name in names])
	for name in names:
		print("%*.*s  %s" % (n, n, name, distname2label(name)))
