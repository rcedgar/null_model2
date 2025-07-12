#!/bin/bash -e

mkdir -p ../log

./run_.bash > ../log/run.stdout 2> ../log/run.stderr

ls -lh ../log/run.stderr
tail ../log/run.stderr
