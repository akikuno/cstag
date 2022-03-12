#!/bin/sh

ref=tests/random_100bp.fa
que=tests/substitution/sub.fq

# PAF
minimap2 --cs "$ref" "$que" >tests/substitution/sub_cs.paf
minimap2 --cs=long "$ref" "$que" >tests/substitution/sub_cslong.paf

# SAM
minimap2 -ax map-ont "$ref" "$que" >tests/substitution/sub.sam
minimap2 -ax map-ont --cs "$ref" "$que" >tests/substitution/sub_cs.sam
minimap2 -ax map-ont --cs=long "$ref" "$que" >tests/substitution/sub_cslong.sam
