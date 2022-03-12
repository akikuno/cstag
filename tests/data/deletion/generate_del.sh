#!/bin/sh

ref=tests/random_100bp.fa
que=tests/deletion/del.fq

# PAF
minimap2 --cs "$ref" "$que" >tests/deletion/del_cs.paf
minimap2 --cs=long "$ref" "$que" >tests/deletion/del_cslong.paf

#SAM
minimap2 -ax map-ont "$ref" "$que" >tests/deletion/del.sam
minimap2 -ax map-ont --cs "$ref" "$que" >tests/deletion/del_cs.sam
minimap2 -ax map-ont --cs=long "$ref" "$que" >tests/deletion/del_cslong.sam

# Check CS tag
cat tests/deletion/del_cs.sam | awk '$1 !~ "@" {print $(NF-1)}'
cat tests/deletion/del_cslong.sam | awk '$1 !~ "@" {print $(NF-1)}'
