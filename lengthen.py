import re
import sys

file = "tests/data/splicing/splicing_cs.sam"
# file = "tests/data/softclip/softclip_no_cs.sam"
with open(file) as f:
    sam = [x.strip() for x in f.readlines()]


header = [s.split("\t") for s in sam  if re.search(r"^@", s)]

contents = [s for s in sam  if not re.search(r"^@", s)]

# ここからfor-loop
content = contents[1]
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

tmp["POS"]
tmp["SEQ"]
tmp["CS"]

tmp1 = re.split('([-+*~:])', tmp["CS"].replace("cs:Z:", ""))[1:]
tmp1 = iter(tmp1)

tmp2 = []
for i,j in zip(tmp1, tmp1):
    tmp2.append(i+j)

idx = 0
cslong = []
for cs in tmp2:
    if cs == "":
        continue
    if cs[0] == ":":
        cs = int(cs[1:]) + idx
        cslong.append(":" + tmp["SEQ"][idx:cs])
        idx += cs
    elif cs[0] == "*":
        cslong.append(cs)
        idx += 1
    elif cs[0] == "-":
        cslong.append(cs)
    elif cs[0] == "+":
        cslong.append(cs)
        idx += len(cs)-2
    elif cs[0] == "~":
        cslong.append(cs)

"cs:Z:" + "".join(cslong).replace(":", "=")