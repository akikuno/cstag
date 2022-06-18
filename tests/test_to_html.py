import os
import filecmp
import tempfile
from src.cstag import to_html


def test_html():
    cs = "cs:Z:=AC+GGG=T-ACGT*at~gt10cg=GNNN"
    output = tempfile.NamedTemporaryFile()
    description = "Example"
    to_html(cs, output, description)

    assert filecmp.cmp(output + ".html", os.path.join("tests", "data", "to_html", "report.html"))
