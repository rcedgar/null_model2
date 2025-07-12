#!/bin/bash

mkdir -p ../big_scop_2.08
cd ../big_scop_2.08

if [ -s dir.rep.scope.2.08-stable.txt ] ; then
	echo "scop 2.08 already downloadd"
else
	for x in \
		https://scop.berkeley.edu/downloads/parse/dir.des.scope.2.08-stable.txt \
		https://scop.berkeley.edu/downloads/parse/dir.cla.scope.2.08-stable.txt \
		https://scop.berkeley.edu/downloads/parse/dir.hie.scope.2.08-stable.txt \
		https://scop.berkeley.edu/downloads/parse/dir.com.scope.2.08-stable.txt \
		https://scop.berkeley.edu/downloads/parse/dir.inc.scope.2.08-stable.txt \
		https://scop.berkeley.edu/downloads/parse/dir.rep.scope.2.08-stable.txt
	do
		wget --no-check-certificate $x
	done
fi
