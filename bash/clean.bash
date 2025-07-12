#!/bin/bash -e

rm -rf ../big_dbs
rm -rf `ls ../big_hits/* | grep -v tm.scop40 | grep -v dali.scop40`
rm -rf ../log
rm -rf ../time
rm -rf ../edf
