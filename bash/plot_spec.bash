#!/bin/bash -e

mkdir -p ../plots

python ../py/plot_dists_spec.py ../plot_specs/$1 ../plots/$1.svg
