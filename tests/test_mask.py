import re
import src.cstag as cstag
import pytest


def test_basic():
    CSTAG = "cs:Z:=ACGT*ac+gg-cc=T"
    QUAL = "AA!!!!AA"
    assert cstag.mask(CSTAG, QUAL) == "cs:Z:=ACNN*an+ng-cc=T"


def test_splicing():
    CSTAG = "cs:Z:=ACGT~gt10~ca=T"
    QUAL = "AA!!A"
    assert cstag.mask(CSTAG, QUAL) == "cs:Z:=ACNN~gt10~ca=T"


def test_threshold_2():
    CSTAG = "cs:Z:=ACGT*ac+gg-cc=T"
    QUAL = r"""01!"#$23"""
    THRESHOLD = 2
    assert cstag.mask(CSTAG, QUAL, THRESHOLD) == "cs:Z:=ACNN*an+gg-cc=T"


def test_threshold_15():
    CSTAG = "cs:Z:=ACGT*ac+gg-cc=T"
    QUAL = r"""01!"#$23"""
    THRESHOLD = 15
    assert cstag.mask(CSTAG, QUAL, THRESHOLD) == "cs:Z:=NCNN*an+ng-cc=T"


def test_error_cstag_short():
    CSTAG = "cs:Z::4*ac+gg-cc:1"
    QUAL = "AA!!!!AA"
    THRESHOLD = 10
    with pytest.raises(Exception) as e:
        _ = cstag.mask(CSTAG, QUAL, THRESHOLD)
        assert str(e.value) == "Error: cs tag must be a long format"


def test_error_threshold_float():
    CSTAG = "cs:Z:=ACGT*ac+gg-cc=T"
    QUAL = "AA!!!!AA"
    THRESHOLD = 9.9
    with pytest.raises(Exception) as e:
        _ = cstag.mask(CSTAG, QUAL, THRESHOLD)
        assert str(e.value) == "Error: threshold must be an integer"


def test_error_threshold_45():
    CSTAG = "cs:Z:=ACGT*ac+gg-cc=T"
    QUAL = "AA!!!!AA"
    THRESHOLD = 45
    with pytest.raises(Exception) as e:
        _ = cstag.mask(CSTAG, QUAL, THRESHOLD)
        assert str(e.value) == "Error: threshold must be within a range between 0 to 40"
