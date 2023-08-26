import pytest
from src.cstag.revcomp import revcomp


# Normal Cases
def test_revcomp_normal():
    # long format
    assert revcomp("cs:Z:=AAAA*ag=CTG") == "cs:Z:=CAG*tc=TTTT"
    assert revcomp("cs:Z:=ACTG+ac=AAAA") == "cs:Z:=TTTT+gt=CAGT"
    assert revcomp("cs:Z:=ACTG-ac=AAAA") == "cs:Z:=TTTT-gt=CAGT"
    assert revcomp("cs:Z:~ag10tc") == "cs:Z:~ga10ct"
    # short format
    assert revcomp("cs:Z::4*ag:3") == "cs:Z::3*tc:4"
    assert revcomp("cs:Z::4+ac") == "cs:Z:+gt:4"
    assert revcomp("cs:Z::4-ac") == "cs:Z:-gt:4"
    assert revcomp("cs:Z:~ag10tc") == "cs:Z:~ga10ct"


# Edge Cases
def test_revcomp_empty():
    assert revcomp("") == ""
    assert revcomp("cs:Z:") == "cs:Z:"


# Special Cases
def test_revcomp_special_chars():
    assert revcomp("cs:Z:+actg-actg") == "cs:Z:-cagt+cagt"


# Invalid Cases
def test_revcomp_invalid():
    with pytest.raises(KeyError):
        revcomp("cs:Z:*zz")
