#!/bin/sh

ref=tests/data/random_100bp.fa
que=tests/data/match/match.fq

#SAM
minimap2 -ax map-ont --cs "$ref" "$que" >tests/data/match/match_cs.sam
minimap2 -ax map-ont --cs=long "$ref" "$que" >tests/data/match/match_cslong.sam

# Check CS tag
cat tests/data/match/match_cs.sam | awk '$1 !~ "@" {print $(NF-1)}'
cat tests/data/match/match_cslong.sam | awk '$1 !~ "@" {print $(NF-1)}'
