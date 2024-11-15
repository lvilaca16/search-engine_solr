#!/bin/bash

#QUERY_PARAMS="config/query_1.json"
COLLECTION="cfdata"

# convert qrels to trec format
./scripts/qrel2trec.py --qrels $1 > qrels_trec.txt

# query solr
./scripts/query_solr.py \
    --query $1 \
    --query_cfg $2 \
    --collection ${COLLECTION} | ./scripts/solr2trec.py > results_trec.txt

# run evaluation pipeline
./scripts/trec_eval/trec_eval qrels_trec.txt results_trec.txt

# cleanup
rm qrels_trec.txt
rm results_trec.txt