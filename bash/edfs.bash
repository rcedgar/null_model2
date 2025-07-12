#!/bin/bash -e

for algo in reseek foldseek dali tm
do
	./edfs_$algo.bash
done
