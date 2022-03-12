#!/bin/sh

ref=tests/data/associate/reference.mfa
que=tests/data/associate/query.fq
minimap2 -ax map-ont "$ref" "$que" >tests/data/associate/query.sam
cat tests/data/associate/query.sam
