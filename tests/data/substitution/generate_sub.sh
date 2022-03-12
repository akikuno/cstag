#!/bin/sh

ref=tests/data/random_100bp.fa
que=tests/data/substitution/sub.fq

# SAM
minimap2 -ax map-ont --cs "$ref" "$que" >tests/data/substitution/sub_cs.sam
minimap2 -ax map-ont --cs=long "$ref" "$que" >tests/data/substitution/sub_cslong.sam
