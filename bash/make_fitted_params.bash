#!/bin/bash -e

python ../py/make_fitted_params.py \
	| tee ../py/fitted_params.py
