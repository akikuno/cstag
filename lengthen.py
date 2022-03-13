import re
import sys

file = "tests/data/softclip/softclip_cs.sam"
# file = "tests/data/softclip/softclip_no_cs.sam"
with open(file) as f:
    sam = [x.strip() for x in f.readlines()]


header = [s.split("\t") for s in sam  if re.search(r"^@", s)]

contents = [s for s in sam  if not re.search(r"^@", s)]

content = contents[0]

if not "cs:Z" in content:
    try:
        raise Exception("Error: cs tag is not found")
    except Exception as e:
        print(e)
        sys.exit(1)


