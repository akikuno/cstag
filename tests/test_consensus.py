import re
import src.cstag as cstag

def test_substitution():
    CSTAG = ["cs:Z:=ACGT", "cs:Z:=AC*gt=T", "cs:Z:=C*gt=T", "cs:Z:=C*gt=T", "cs:Z:=ACT+ccc=T"]
    CIGAR = ["4M","4M","1S3M", "3M", "3M3I1M"]
    POS = [1,1,1,2,1]
    assert cstag.consensus(CSTAG, CIGAR, POS) == "cs:Z:=AC*gt=T"

