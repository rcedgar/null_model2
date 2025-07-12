#!/bin/bash -e

ref=$1
target=$2
xrange=$3
yrange=$4
prior=$5

if [ -z "$prior" ] ; then
	echo $0: Missing arg
	exit 1
fi

outdir=../predict_P_F_score
mkdir -p $outdir

out=$outdir/ref_${ref}_target_${target}
plot=$outdir/ref_${ref}_target_${target}.svg

python ../py/predict_P_F_score.py \
	--edf_ref ../edf/$ref \
	--edf_target ../edf/$target \
	--prior_pf $prior \
	--output $out \
	--xrange $xrange \
	--yrange $yrange \
	--plot $plot

ls -lh $out $plot
