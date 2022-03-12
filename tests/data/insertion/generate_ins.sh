#!/bin/sh

ref=tests/data/random_100bp.fa
que=tests/data/insertion/ins.fq

# SAM
minimap2 -ax map-ont --cs "$ref" "$que" >tests/data/insertion/ins_cs.sam
minimap2 -ax map-ont --cs=long "$ref" "$que" >tests/data/insertion/ins_cslong.sam
