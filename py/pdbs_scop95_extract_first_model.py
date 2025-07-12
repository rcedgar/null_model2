#!/usr/bin/python3

import os
import sys

indir = "./"
outdir = "fixed_pdbs/"
lookupfn = "scop95.lookup"

doms = set()
for line in open(lookupfn):
	dom = line.split('\t')[0]
	doms.add(dom)

os.system("rm -rf " + outdir)
os.system("mkdir -p " + outdir)

ents_fn = "ent.files"
n = 0
for ent_fn in open(ents_fn):
	ent_fn = ent_fn[:-1]
	dom = ent_fn.split('/')[-1].replace(".ent", "")
	if not dom in doms:
		continue
	n += 1
	if n%100 == 0:
		sys.stderr.write("%d %s\r" % (n, dom))
	in_fn = indir + ent_fn
	model_found = True
	fixed_pdb_fn = outdir + dom + ".pdb"
	fixed_file = open(fixed_pdb_fn, "w")
	for line in open(in_fn):
		if line.startswith("MODEL "):
			if model_found:
				break
			model_found = True
			continue
		if line.startswith("ENDMDL"):
			break
		fixed_file.write(line)
	fixed_file.close()
sys.stderr.write("%d %s\n" % (n, dom))
