#!/bin/bash -e

name=null_model2

now=`date "+%Y-%m-%d-%H_%S"`

date "+%Y-%m-%d-%H_%S" \
	> ../sync_log/$now.started

aws s3 sync .. s3://serratus-rce-mirror/$name \
	> /tmp/sync.$now.stdout \
	2> /tmp/sync.$now.stderr

mkdir -p ../sync_log

mv -v /tmp/sync.$now.stderr \
	../sync_log/

grep upload /tmp/sync.$now.stdout \
	| sed "-es/Completed.*calculating.....//" \
	> sync.$now.uploads

date "+%Y-%m-%d-%H_%S" \
	> ../sync_log/$now.finished

echo
echo
echo =============================
echo sync $now finished
echo =============================
