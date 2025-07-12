#!/usr/bin/python3

import sys
import os
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import colnames

def set_size(w, h, ax=None):
	""" w, h: width, height in inches """
	if not ax: ax=plt.gca()
	l = ax.figure.subplotpars.left
	r = ax.figure.subplotpars.right
	t = ax.figure.subplotpars.top
	b = ax.figure.subplotpars.bottom
	figw = float(w)/(r-l)
	figh = float(h)/(t-b)
	ax.figure.set_size_inches(figw, figh)

def read_dist(fn, distname):
	bin_mids = []
	fld_nr = None
	v = []
	for line in open(fn):
		if line.startswith('#'):
			continue
		if fld_nr is None:
			hdr = line[:-1].split('\t')
			assert hdr[0] == "binmids"
			for i in range(len(hdr)):
				if hdr[i] == distname:
					fld_nr = i
					break
			if fld_nr is None:
				assert False, "distname=%s not found in fn=%s" % (distname, fn)
			continue
		if len(line.strip()) == 0:
			continue
		flds = line[:-1].split('\t')
		bin_mid = float(flds[0])
		x = float(flds[fld_nr])

		bin_mids.append(bin_mid)
		v.append(x)

	return bin_mids, np.array(v, dtype=np.float32)

subplot_width = 3
subplot_height = 2.5
name_distname2label = {}
name_distname2style = {}
name_distname2fn = {}

curr_row = None
curr_col = None
nr_rows = 0
nr_cols = 0
row_col2distname = {}
row_col2names = {}
row_col2specs = {}
row_col2title = {}
row_col2logy = {}
row_col2xlim = {}
row_col2ylim = {}

def set_cols_per_row(n):
	global nr_cols, nr_rows
	nr_cols = n
	nr_rows = 1

def reset():
	global curr_row
	global curr_col
	global nr_rows
	global nr_cols
	global row_col2distname
	global row_col2names
	global row_col2specs
	global row_col2title
	global row_col2logy
	global row_col2xlim
	global row_col2ylim

	nr_rows = 0
	curr_row = None
	curr_col = None
	row_col2distname = {}
	row_col2names = {}
	row_col2specs = {}
	row_col2title = {}
	row_col2logy = {}
	row_col2xlim = {}
	row_col2ylim = {}

def set_subplot_width(w):
	global subplot_width
	subplot_width = w

def add_fn_distname(name, fn, distname, label, style = dict()):
	try:
		f = open(fn)
	except:
		f = None
	if f is None:
		assert False, "File not found %s" % fn
	else:
		f.close()
	name_distname = (name, distname)
	name_distname2fn[name_distname] = fn
	name_distname2label[name_distname] = label
	name_distname2style[name_distname] = style

def add_subplot(distname, title, logy, xlim = None, ylim = None):
	global nr_rows, nr_cols, curr_row, curr_col

	if nr_cols is None:
		set_cols_per_row(2)

	if curr_col is None:
		curr_col = 0
		curr_row = 0
	else:
		curr_col += 1
		if curr_col == nr_cols:
			curr_col = 0
			curr_row += 1
			nr_rows = curr_row + 1

	row_col = (curr_row, curr_col)
	row_col2distname[row_col] = distname
	row_col2title[row_col] = title
	row_col2logy[row_col] = logy
	row_col2xlim[row_col] = xlim
	row_col2ylim[row_col] = ylim
	row_col2names[row_col] = []
	row_col2specs[row_col] = []

def add_subplot_line(name, spec = None):
	row = curr_row
	col = curr_col
	row_col = (row, col)
	row_col2names[row_col].append(name)
	row_col2specs[row_col].append(spec)

def plot_dists(svg_fn):
	matplotlib.use('Agg')
	fig, axs = plt.subplots(nr_rows, nr_cols)
	print("%d rows x %d cols" % (nr_rows, nr_cols))
	for row in range(nr_rows):
		for col in range(nr_cols):
			row_col = (row, col)
			if nr_rows == 1 and nr_cols > 1:
				ax = axs[col]
			elif nr_rows > 1 and nr_cols == 1:
				ax = axs[row]
			elif nr_rows > 1 or nr_cols > 1:
				ax = axs[row][col]
			else:
				ax = axs

			distname = row_col2distname[row_col]
			title = row_col2title[row_col]
			logy = row_col2logy[row_col]
			xlim = row_col2xlim[row_col]
			ylim = row_col2ylim[row_col]
			names = row_col2names[row_col]
			specs = row_col2specs[row_col]
			nr_lines = len(names)

			ax.set_title(title)
			if distname == "CatE":
				ax.set_xlabel("Cat coverage")
				ax.set_ylabel("CatEPQ")
				for idx in range(nr_lines):
					name = names[idx]
					name_distname = (name, "CatE")
					name_distname_sens = (name, "cate_sens")
					name_distname_fpepq = (name, "cate_epq")
					fn_sens = name_distname2fn.get(name_distname_sens)
					if fn_sens is None:
						assert False, "name_distname2fn.get(%s)" % str(name_distname_sens)
					fn_fpepq = name_distname2fn.get(name_distname_fpepq)
					if fn_fpepq is None:
						assert False, "name_distname2fn.get(%s)" % str(name_distname_fpepq)
					label = name_distname2label[name_distname_sens]
					style = specs[idx]
					if style is None:
						style = dict()
					bin_mids, PDF_sens = read_dist(fn_sens, "cate_sens")
					bin_mids_fpepq, PDF_fpepq = read_dist(fn_sens, "cate_epq")
					assert bin_mids_fpepq == bin_mids

					ax.set_yscale('log')
					ax.set_xlim([0, 1])
					ax.set_ylim([0.00001, 1])
					ax.plot(PDF_sens, PDF_fpepq, label=label, **style)
				ax.legend()
				continue

			elif distname == "CVE":
				ax.set_xlabel("Sensitivity")
				ax.set_ylabel("FPEPQ")
				for idx in range(nr_lines):
					name = names[idx]
					name_distname = (name, "CVE")
					name_distname_sens = (name, "cve_sens")
					name_distname_fpepq = (name, "cve_epq")
					fn_sens = name_distname2fn.get(name_distname_sens)
					if fn_sens is None:
						assert False, "name_distname2fn.get(%s)" % str(name_distname_sens)
					fn_fpepq = name_distname2fn.get(name_distname_fpepq)
					if fn_fpepq is None:
						assert False, "name_distname2fn.get(%s)" % str(name_distname_fpepq)
					label = name_distname2label[name_distname_sens]
					style = specs[idx]
					if style is None:
						style = dict()
					bin_mids, PDF_sens = read_dist(fn_sens, "cve_sens")
					bin_mids_fpepq, PDF_fpepq = read_dist(fn_sens, "cve_epq")
					assert bin_mids_fpepq == bin_mids

					ax.set_yscale('log')
					ax.set_xlim(xlim)
					ax.set_ylim(ylim)
					ax.plot(PDF_sens, PDF_fpepq, label=label, **style)
				ax.legend()
				continue
			else:
				ax.set_xlabel("Score")
				ax.set_ylabel(distname)
			if logy:
				ax.set_yscale('log')
			if not xlim is None:
				ax.set_xlim(xlim)
			if not ylim is None:
				ax.set_ylim(ylim)

			for idx in range(nr_lines):
				name = names[idx]
				name_distname = (name, distname)
				fn = name_distname2fn.get(name_distname)
				if fn is None:
					assert False, "name_distname2fn.get(%s)" % str(name_distname)
				label = name_distname2label[name_distname]
				style = specs[idx]
				if style is None:
					style = name_distname2style[name_distname]
				bin_mids, PDF = read_dist(fn, distname)

				ax.plot(bin_mids, PDF, label=label, **style)
			ax.legend()

	sys.stderr.write(svg_fn + '\n')
	fig_width = nr_cols*subplot_width
	fig_height = nr_rows*subplot_height
	set_size(fig_width, fig_height)
	fig.tight_layout()
	fig.savefig(svg_fn)

distnames = colnames.get_colnames()

style_all =		{ "color" : "black", "linestyle" : "solid" }
style_2 =		{ "color" : "darkgray", "linestyle" : "dashed" }
style_4 =		{ "color" : "darkgray", "linestyle" : "dotted" }
style_8 =		{ "color" : "lightgray", "linestyle" : "dotted" }

style_a =	{ "color" : "orange"  }
style_b =	{ "color" : "green"  }
style_c =	{ "color" : "blue"  }
style_d =	{ "color" : "magenta"  }

style_a2 =	{ "color" : "orange", "linestyle": "dashed" }
style_b2 =	{ "color" : "green",  "linestyle": "dashed" }
style_c2 =	{ "color" : "blue",  "linestyle": "dashed" }
style_d2 =	{ "color" : "magenta",  "linestyle": "dashed" }

style_orange =	{ "color" : "orange"  }
style_blue =	{ "color" : "blue"  }

def init_reseek():
	for distname in distnames:
		add_fn_distname("scop95", "../edf/scop95.reseek", distname, "SCOP95", style_all)
		add_fn_distname("scop95_n1", "../edf/scop95.reseek", distname, "SCOP95 (N=1)", style_all)
		add_fn_distname("scop95_n3", "../edf/scop40.reseek", distname, "SCOP95 (N~3)", style_all)
		add_fn_distname("scop95/2", "../edf/scop95.reseek.n2.avg", distname, "SCOP95 N=1/2", style_2)
		add_fn_distname("scop95/4", "../edf/scop95.reseek.n4.avg", distname, "SCOP95 N=1/4", style_4)
		add_fn_distname("scop95/8", "../edf/scop95.reseek.n8.avg", distname, "SCOP95 N=1/8", style_8)
		add_fn_distname("scop95/sf2", "../edf/scop95.reseek.sf2.avg", distname, "SCOP95 SF=1/2", style_2)
		add_fn_distname("scop95/sf4", "../edf/scop95.reseek.sf4.avg", distname, "SCOP95 SF=1/4", style_4)
		add_fn_distname("scop95/sf8", "../edf/scop95.reseek.sf8.avg", distname, "SCOP95 SF=1/8", style_8)
		add_fn_distname("scop95/40%", "../edf/scop95.reseek.cluster40", distname, "SCOP95/40%", style_2)
		add_fn_distname("scop95/70%", "../edf/scop95.reseek.cluster70", distname, "SCOP95/70%", style_2)

		add_fn_distname("scop40", "../edf/scop40.reseek", distname, "SCOP40", style_all)
		add_fn_distname("scop40_n1", "../edf/scop40.reseek", distname, "SCOP40 (N=1)", style_all)
		add_fn_distname("scop40/2", "../edf/scop40.reseek.n2.avg", distname, "SCOP40 N=1/2", style_2)
		add_fn_distname("scop40/4", "../edf/scop40.reseek.n4.avg", distname, "SCOP40 N=1/4", style_4)
		add_fn_distname("scop40/8", "../edf/scop40.reseek.n8.avg", distname, "SCOP40 N=1/8", style_8)
		add_fn_distname("scop40/sf2", "../edf/scop40.reseek.sf2.avg", distname, "SCOP40 SF=1/2", style_2)
		add_fn_distname("scop40/sf4", "../edf/scop40.reseek.sf4.avg", distname, "SCOP40 SF=1/4", style_4)
		add_fn_distname("scop40/sf8", "../edf/scop40.reseek.sf8.avg", distname, "SCOP40 SF=1/8", style_8)

def init_algo(algo):
	if algo == "reseek":
		init_reseek()
		return

	for distname in distnames:
		add_fn_distname("scop40", "../edf/scop40." + algo, distname, "SCOP40", style_all)
		add_fn_distname("scop40_n1", "../edf/scop40." + algo, distname, "SCOP40 (N=1)", style_all)
		add_fn_distname("scop40/2", "../edf/scop40." + algo + ".n2.avg", distname, "SCOP40 N=1/2", style_2)
		add_fn_distname("scop40/4", "../edf/scop40." + algo + ".n4.avg", distname, "SCOP40 N=1/4", style_4)
		add_fn_distname("scop40/8", "../edf/scop40." + algo + ".n8.avg", distname, "SCOP40 N=1/8", style_8)
		add_fn_distname("scop40/sf2", "../edf/scop40." + algo + ".sf2.avg", distname, "SCOP40 SF=1/2", style_2)
		add_fn_distname("scop40/sf4", "../edf/scop40." + algo + ".sf4.avg", distname, "SCOP40 SF=1/4", style_4)
		add_fn_distname("scop40/sf8", "../edf/scop40." + algo + ".sf8.avg", distname, "SCOP40 SF=1/8", style_8)
