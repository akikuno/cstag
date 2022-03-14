#!/bin/sh

ref=tests/data/random_100bp.fa
que=tests/data/subindel/subindel.fq

# SAM
minimap2 -ax map-ont --cs "$ref" "$que" >tests/data/subindel/subindel_cs.sam
minimap2 -ax map-ont --cs=long "$ref" "$que" >tests/data/subindel/subindel_cslong.sam
