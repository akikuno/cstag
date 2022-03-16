#!/bin/sh

ref=tests/data/random_100bp.fa
ref_10bp=tests/data/random_100bp_plus10bp.fa
que=tests/data/consensus/subindel.fq

# SAM
minimap2 -ax map-ont --cs "$ref" "$que" >tests/data/consensus/subindel_cs.sam
minimap2 -ax map-ont --cs=long "$ref" "$que" >tests/data/consensus/subindel_cslong.sam
minimap2 -ax map-ont --cs "$ref_10bp" "$que" >tests/data/consensus/subindel_cs_plus10bp.sam
minimap2 -ax map-ont --cs=long "$ref_10bp" "$que" >tests/data/consensus/subindel_cslong_plus10bp.sam
