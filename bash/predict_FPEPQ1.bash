#!/bin/bash -e

xrange=$1
PF=$2
ref=$3
target=$4
loglin=$5

if [ xloglin == x ] ; then
	echo $0: Missing arg
fi

name=ref_$ref.target_$target

mkdir -p ../predict_FPEPQ
cd ../predict_FPEPQ

python ../py/predict_FPEPQ.py \
	--edf_ref ../edf/$ref \
	--edf_target ../edf/$target \
	--loglin ../fit_loglin/$loglin.tsv \
	--xrange $xrange \
	--plot $name.svg,$name.png \
	--output $name.tsv \
	--target_prior_pf $PF
