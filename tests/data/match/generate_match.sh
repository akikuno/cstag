#!/bin/sh

ref=tests/random_100bp.fa
que=tests/match/match.fq

#SAM
minimap2 -ax map-ont --cs "$ref" "$que" >tests/match/match_cs.sam
minimap2 -ax map-ont --cs=long "$ref" "$que" >tests/match/match_cslong.sam

# Check CS tag
cat tests/match/match_cs.sam | awk '$1 !~ "@" {print $(NF-1)}'
cat tests/match/match_cslong.sam | awk '$1 !~ "@" {print $(NF-1)}'
