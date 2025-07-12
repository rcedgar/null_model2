#!/bin/bash -e

mkdir -p ../big_hits
cd ../big_hits

# reseek-v2.4 \
#	-search ../RESEEKDB/cath40.bca \
#	-db ../RESEEKDB/cath40.bca \
#	-output reseek_search/reseek_cath40_vs_cath40.tsv \
#	-sensitive \
#	-threads 48 \
#	-evalue 9999

aws s3 cp s3://serratus-reseek/reseek_search/reseek_cath40_vs_cath40_sensitive.tsv reseek_sensitive.cath40.tmp

##############################################################
# Remove AQ field and delete _A chain id. added to CATH labels
##############################################################
cut -f2,3,4 reseek_sensitive.cath40.tmp \
	| sed "-es/_.\t/\t/g" \
	> reseek.cath40
rm -f reseek_sensitive.cath40.tmp
