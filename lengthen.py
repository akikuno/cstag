import re
import sys

file = "tests/data/softclip/softclip_cs.sam"
# file = "tests/data/softclip/softclip_no_cs.sam"
with open(file) as f:
    sam = [x.strip() for x in f.readlines()]


header = [s.split("\t") for s in sam  if re.search(r"^@", s)]

contents = [s for s in sam  if not re.search(r"^@", s)]

# ここからfor-loop
content = contents[0]
# for content in contents:

if not "cs:Z" in content:
    try:
        raise Exception("Error: cs tag is not found")
    except Exception as e:
        print(e)
        sys.exit(1)

names = ["QNAME", "FLAG", "RNAME", "POS", "MAPQ", "CIGAR", "RNEXT", "PNEXT", "TLEN", "SEQ", "QUAL"]

tmp = {n:c for n,c in zip(names, content.split("\t"))}
tmp.update({"CS": c for c in content.split("\t") if re.search(r"^cs:Z",c)})

tmp