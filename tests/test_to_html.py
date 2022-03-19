import re
import os
import filecmp
from src.cstag import to_html

cs = "cs:Z:=AC+GGG=T-ACGT*at~gt10cg=GNNN"
output = os.path.join("/tmp", "report")
description = "Example"
to_html(cs, output, description)

assert filecmp.cmp(
    output + ".html", os.path.join("tests", "data", "to_html", "report.html")
)
