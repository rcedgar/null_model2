dbname2size = {}

dbname2size["afdb"] = 214000000
dbname2size["afdb50"] = 53665860
dbname2size["afdb100k"] = 100000
dbname2size["pdb"] = 884129
dbname2size["bfvd"] = 347514
dbname2size["scop40"] = 11211
dbname2size["cath40"] = 34647
dbname2size["scop40c"] = 8340
dbname2size["scop40n2"] = 11211//2
dbname2size["scop40n4"] = 11211//4
dbname2size["scop40sf2"] = 11211//2
dbname2size["scop40sf4"] = 11211//4
dbname2size["scop40_div2"] = 11211//2
dbname2size["scop40_div4"] = 11211//4
dbname2size["scop40_div8"] = 11211//8
dbname2size["scop40_div16"] = 11211//16
dbname2size["scop40x2"] = 22422
dbname2size["scop40x4"] = 56055
dbname2size["scop40x8"] = 89688
dbname2size["scop95"] = 28284
dbname2size["scop95_cluster40"] = 15696
dbname2size["scop95_cluster70"] = 22188

def get_names(hitsfn, lookupfn):
	fn = hitsfn.split('/')[-1]
	flds = fn.split('.')
	if len(flds) == 2:
		algo = flds[0]
		assert flds[1] == "scop40"
		qname = "scop40"
		dbname = "scop40"
	elif len(flds) == 3:
		algo = flds[0]
		qname = flds[1]
		dbname = flds[2]
	else:
		assert False

	if not lookupfn is None:
		if dbname == "scop40" and lookupfn.find("scop40c") >= 0:
			assert qname == "scop40"
			qname = "scop40c"
			dbname = "scop40c"
		elif lookupfn.find("cluster") > 0:
			name = lookupfn.split('/')[-1].split('.')[0]
			qname = name
			dbname = name

	if qname is None or dbname is None:
		assert False
	return qname, dbname
