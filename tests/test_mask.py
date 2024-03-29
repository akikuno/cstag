import src.cstag as cstag
import pytest


def test_basic():
    CSTAG = "=ACGT*ac+gg-cc=T"
    CIGAR = "5M2I2D1M"
    QUAL = "AA!!!!AA"
    assert cstag.mask(CSTAG, CIGAR, QUAL) == "=ACNN*an+ng-cc=T"


def test_basic_with_prefix():
    CSTAG = "cs:Z:=ACGT*ac+gg-cc=T"
    CIGAR = "5M2I2D1M"
    QUAL = "AA!!!!AA"
    assert cstag.mask(CSTAG, CIGAR, QUAL, prefix=True) == "cs:Z:=ACNN*an+ng-cc=T"


def test_all_n():
    CSTAG = "=ACGT"
    CIGAR = "4M"
    QUAL = "!!!!"
    assert cstag.mask(CSTAG, CIGAR, QUAL) == "=NNNN"


def test_softclip():
    CSTAG = "=ACGT*ac+gg-cc=T"
    CIGAR = "2S5M2I2D1M"
    QUAL = "AAAA!!!!AA"
    assert cstag.mask(CSTAG, CIGAR, QUAL) == "=ACNN*an+ng-cc=T"


def test_splicing():
    CSTAG = "=ACGT~gt10ca=T"
    CIGAR = "5M10N1M"
    QUAL = "AA!!A"
    assert cstag.mask(CSTAG, CIGAR, QUAL) == "=ACNN~gt10ca=T"


def test_threshold_2():
    CSTAG = "=ACGT*ac+gg-cc=T"
    CIGAR = "5M2I2D1M"
    QUAL = r"""01!"#$23"""
    THRESHOLD = 2
    assert cstag.mask(CSTAG, CIGAR, QUAL, THRESHOLD) == "=ACNN*an+gg-cc=T"


def test_threshold_15():
    CSTAG = "=ACGT*ac+gg-cc=T"
    CIGAR = "5M2I2D1M"
    QUAL = r"""01!"#$23"""
    THRESHOLD = 15
    assert cstag.mask(CSTAG, CIGAR, QUAL, THRESHOLD) == "=NCNN*an+ng-cc=T"


def test_error_cstag_short():
    CSTAG = ":4*ac+gg-cc:1"
    CIGAR = "5M2I2D1M"
    QUAL = "AA!!!!AA"
    THRESHOLD = 10
    with pytest.raises(Exception) as e:
        _ = cstag.mask(CSTAG, CIGAR, QUAL, THRESHOLD)
        assert str(e.value) == "Error: cs tag must be a long format"


def test_error_threshold_float():
    CSTAG = "=ACGT*ac+gg-cc=T"
    CIGAR = "5M2I2D1M"
    QUAL = "AA!!!!AA"
    THRESHOLD = 9.9
    with pytest.raises(Exception) as e:
        _ = cstag.mask(CSTAG, CIGAR, QUAL, THRESHOLD)
        assert str(e.value) == "Error: threshold must be an integer"


def test_error_threshold_45():
    CSTAG = "=ACGT*ac+gg-cc=T"
    CIGAR = "5M2I2D1M"
    QUAL = "AA!!!!AA"
    THRESHOLD = 45
    with pytest.raises(Exception) as e:
        _ = cstag.mask(CSTAG, CIGAR, QUAL, THRESHOLD)
        assert str(e.value) == "Error: threshold must be within a range between 0 to 40"
