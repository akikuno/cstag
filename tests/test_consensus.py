import re
import src.cstag as cstag


def test_substitution():
    CSTAG = [
        "cs:Z:=ACGT",
        "cs:Z:=AC*gt=T",
        "cs:Z:=C*gt=T",
        "cs:Z:=C*gt=T",
        "cs:Z:=ACT+ccc=T",
    ]
    CIGAR = ["4M", "4M", "1S3M", "3M", "3M3I1M"]
    POS = [1, 1, 1, 2, 1]
    assert cstag.consensus(CSTAG, CIGAR, POS) == "cs:Z:=AC*gt=T"


def test_insertion():
    CSTAG = ["cs:Z:=ACGT", "cs:Z:=AC+ggggg=GT", "cs:Z:=C+ggggg=GT", "cs:Z:=C+ggggg=GT"]
    CIGAR = ["4M", "2M5I1M", "1S5I3M", "1M5I1M"]
    POS = [1, 1, 1, 2]
    assert cstag.consensus(CSTAG, CIGAR, POS) == "cs:Z:=AC+ggggg=GT"


def test_deletion():
    CSTAG = ["cs:Z:=ACGT", "cs:Z:=AC-ggggg=GT", "cs:Z:=C-ggggg=GT", "cs:Z:=C-ggggg=GT"]
    CIGAR = ["4M", "2M5D1M", "1S5D3M", "1M5D1M"]
    POS = [1, 1, 1, 2]
    assert cstag.consensus(CSTAG, CIGAR, POS) == "cs:Z:=AC-ggggg=GT"


def test_softclip():
    CSTAG = ["cs:Z:=ACGT", "cs:Z:=CGT", "cs:Z:=GT"]
    CIGAR = ["4M", "1S3M", "2S2M"]
    POS = [1, 1, 1]
    assert cstag.consensus(CSTAG, CIGAR, POS) == "cs:Z:=NCGT"


def test_splicing():
    CSTAG = [
        "cs:Z:=ACGT",
        "cs:Z:=AC~gc100ag=T",
        "cs:Z:=C~gc100ag=T",
        "cs:Z:=C~gc100ag=T",
    ]
    CIGAR = ["4M", "2M100N1M", "1S100N3M", "1M100N1M"]
    POS = [1, 1, 1, 2]
    assert cstag.consensus(CSTAG, CIGAR, POS) == "cs:Z:=AC~gc100ag=T"
