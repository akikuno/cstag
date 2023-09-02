import pytest
from src.cstag.revcomp import revcomp


# Normal Cases
def test_revcomp_normal():
    # long format
    assert revcomp("=AAAA*ag=CTG") == "=CAG*tc=TTTT"
    assert revcomp("=ACTG+ac=AAAA") == "=TTTT+gt=CAGT"
    assert revcomp("=ACTG-ac=AAAA") == "=TTTT-gt=CAGT"
    assert revcomp("~ag10tc") == "~ga10ct"
    # short format
    assert revcomp(":4*ag:3") == ":3*tc:4"
    assert revcomp(":4+ac") == "+gt:4"
    assert revcomp(":4-ac") == "-gt:4"
    assert revcomp("~ag10tc") == "~ga10ct"


def test_revcomp_prefix():
    assert revcomp("=AAAA*ag=CTG", prefix=True) == "cs:Z:=CAG*tc=TTTT"


# Edge Cases
def test_revcomp_empty():
    assert revcomp("") == ""
    assert revcomp("cs:Z:") == ""


# Special Cases
def test_revcomp_special_chars():
    assert revcomp("+actg-actg") == "-cagt+cagt"


# Invalid Cases
def test_revcomp_invalid():
    with pytest.raises(KeyError):
        revcomp("cs:Z:*zz")
