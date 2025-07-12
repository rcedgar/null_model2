#!/bin/bash -e

alns=../big_foldseek_suppmat_alns
mkdir -p $alns
cd $alns

wget https://wwwuser.gwdguser.de/~compbiol/foldseek/scop.benchmark.result.tar.gz
tar -zxf scop.benchmark.result.tar.gz
