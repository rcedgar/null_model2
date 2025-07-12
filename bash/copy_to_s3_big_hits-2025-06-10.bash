#!/bin/bash -e

if [ ! -s ../tmp/big_hits-2025-06-10.tz ] ; then
	tar -h --hard-dereference -zcvf ../tmp/big_hits-2025-06-10.tz .
fi

aws s3 cp ../tmp/big_hits-2025-06-10.tz s3://serratus-reseek/big_hits/
aws s3 cp $0 s3://serratus-reseek/big_hits/bash

