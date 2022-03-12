#!/bin/sh

ref=tests/data/random_100bp.fa
que=tests/data/softclip/softclip.fq

#SAM
minimap2 -ax map-ont --cs "$ref" "$que" >tests/data/softclip/softclip_cs.sam
minimap2 -ax map-ont --cs=long "$ref" "$que" >tests/data/softclip/softclip_cslong.sam

# Check CS tag
cat tests/data/softclip/softclip_cs.sam | awk '$1 !~ "@" {print $(NF-1)}'
cat tests/data/softclip/softclip_cslong.sam | awk '$1 !~ "@" {print $(NF-1)}'
