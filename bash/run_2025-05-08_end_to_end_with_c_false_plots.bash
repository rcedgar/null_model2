#!/bin/bash

# 05276a0 + 1

name=2025-05-08_end_to_end_with_c_false_plots
rundir=../runs/$name

rm -rf $rundir
mkdir -p $rundir
mkdir -p ../log
rm -f ../log/steps.log

echo download_dali_and_tm_hits.bash | tee -a ../log/steps.log
./download_dali_and_tm_hits.bash

echo setups | tee -a ../log/steps.log
./setup_cath40.bash
./setup_scop40.bash
./setup_scop95.bash
./setup_scop40x8.bash

echo reseek_searches | tee -a ../log/steps.log
./reseek_search.bash cath40
./reseek_search.bash scop40
./reseek_search.bash scop95
./reseek_search_x8.bash

echo reseek_searches | tee -a ../log/steps.log
./foldseek_search.bash cath40
./foldseek_search.bash scop40
./foldseek_search.bash scop95
./foldseek_search_scop40x8.bash

for algo in reseek reseekts foldseek foldseekb dali tm
do
	echo edfs_$algo | tee -a ../log/steps.log
	./edfs_$algo.bash
done

./c_false_plots.bash

date \
	> $rundir/date.txt

git log head \
	> $rundir/git_log.txt

cp -vr ../plots $rundir
cp -vr ../edf $rundir

./sync_to_s3.bash