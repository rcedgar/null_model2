#!/bin/bash -e

# Use nohup ... & or screen to run in background

name=null_model

now=`date "+%Y-%m-%d-%H_%S"`

aws s3 sync .. s3://serratus-rce-mirror/$name --dryrun \
	> /tmp/sync_dryrun.$now.stdout \
	2> /tmp/sync_dryrun.$now.stderr

echo
echo
echo =============================
echo sync dryrun $now finished
echo =============================
