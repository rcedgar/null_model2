#!/bin/bash -e

mkdir -p ../evalue_vs_epq
cd ../evalue_vs_epq

python ../py/plot_evalue_vs_epq_foldseek_rescale.py \
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
	--dbsizes $((11211*8)) $((11211*4)) $((11211*2)) $((11211)) $((11211/2)) $((11211/4)) \
	--title "Foldseek" \
	--plot foldseek_scop40nx_rescale_default.svg foldseek_scop40nx_rescale_default.png \
	--yrange 1e-2:10 \
	--xrange 1e-2:10
