#!/bin/sh

ref=tests/data/random_100bp.fa
que=tests/data/deletion/del.fq

minimap2 -ax map-ont --cs "$ref" "$que" >tests/data/deletion/del_cs.sam
minimap2 -ax map-ont --cs=long "$ref" "$que" >tests/data/deletion/del_cslong.sam
