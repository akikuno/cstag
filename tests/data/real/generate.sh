#!/bin/sh

# zcat tests/data/real/barcode32.fq.gz | head -n 400 > tests/data/real/barcode32.fq
ref=tests/data/real/tyr.fa
que=tests/data/real/barcode32.fq

#ls -lh  tests/data/real/barcode32.fq
#SAM
minimap2 -ax map-ont --cs "$ref" "$que" >tests/data/real/tyr_cs.sam
minimap2 -ax map-ont --cs=long "$ref" "$que" >tests/data/real/tyr_cslong.sam

# ls -lh tests/data/real
