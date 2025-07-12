#!/bin/bash -e

mkdir -p ../evalue_vs_epq
cd ../evalue_vs_epq

python ../py/plot_evalue_vs_epq.py \
	--edfs \
		../edf/foldseek_default.scop40.scop40x8.scop40 \
		../edf/foldseek_default.scop40.scop40x4.scop40 \
		../edf/foldseek_default.scop40.scop40x2.scop40 \
		../edf/foldseek_default.scop40.scop40.scop40 \
		../edf/foldseek_default.scop40.scop40_div2.scop40_div2 \
		../edf/foldseek_default.scop40.scop40_div4.scop40_div4 \
	--labels \
		"SCOP40x8" \
		"SCOP40x4" \
		"SCOP40x2" \
		"SCOP40" \
		"SCOP40/2" \
		"SCOP40/4" \
	--title "Foldseek (default)" \
	--plot foldseek_default_scop40nx.svg foldseek_default_scop40nx.png \
	--yrange 1e-3:1000 \
	--xrange 1e-10:10

python ../py/plot_evalue_vs_epq.py \
	--edfs \
		../edf/foldseek_exhaustive.scop40.scop40x8.scop40 \
		../edf/foldseek_exhaustive.scop40.scop40x4.scop40 \
		../edf/foldseek_exhaustive.scop40.scop40x2.scop40 \
		../edf/foldseek_exhaustive.scop40.scop40.scop40 \
		../edf/foldseek_exhaustive.scop40.scop40_div2.scop40_div2 \
		../edf/foldseek_exhaustive.scop40.scop40_div4.scop40_div4 \
	--labels \
		"SCOP40x8" \
		"SCOP40x4" \
		"SCOP40x2" \
		"SCOP40" \
		"SCOP40/2" \
		"SCOP40/4" \
	--title "Foldseek (exhaustive)" \
	--plot foldseek_exhaustive_scop40nx.svg foldseek_exhaustive_scop40nx.png \
	--yrange 1e-3:1000 \
	--xrange 1e-10:10

python ../py/plot_evalue_vs_epq.py \
	--edfs \
		../edf/reseek_sensitive_evalue.scop40.scop40x8.scop40 \
		../edf/reseek_sensitive_evalue.scop40.scop40x4.scop40 \
		../edf/reseek_sensitive_evalue.scop40.scop40x2.scop40 \
		../edf/reseek_sensitive_evalue.scop40.scop40.scop40 \
		../edf/reseek_sensitive_evalue.scop40.scop40_div2.scop40_div2\
		../edf/reseek_sensitive_evalue.scop40.scop40_div4.scop40_div4 \
	--labels \
		"SCOP40x8" \
		"SCOP40x4" \
		"SCOP40x2" \
		"SCOP40" \
		"SCOP40/2" \
		"SCOP40/4" \
	--title "Reseek" \
	--plot reseek_scop40nx.svg reseek_scop40nx.png \
	--yrange 1e-2:100 \
	--xrange 1e-3:10

mkdir -p ../summary_pngs
montage -geometry 1000x1000 *.png ../summary_pngs/evalue_vs_epq.png
