#!/bin/sh

###########################################################
# Generate test data for real samples
# FASTQ = Nanopore reads in the Tyr genomic region of wild-type mice (C57B6/J)
###########################################################

ref=tests/data/real/tyr.fa
que=tests/data/real/tyr_control.fq

minimap2 -ax map-ont --cs "$ref" "$que" >tests/data/real/tyr_cs.sam
minimap2 -ax map-ont --cs=long "$ref" "$que" >tests/data/real/tyr_cslong.sam
