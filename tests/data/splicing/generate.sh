#!/bin/sh

ref=tests/data/random_1500bp.fa
que=tests/data/splicing/splicing.fq

#SAM
minimap2 -ax splice --cs "$ref" "$que" >tests/data/splicing/splicing_cs.sam
minimap2 -ax splice --cs=long "$ref" "$que" >tests/data/splicing/splicing_cslong.sam
