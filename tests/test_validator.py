import pytest
from src.cstag.utils.validator import (
    validate_cs_tag,
    validate_short_format,
    validate_long_format,
    validate_threshold,
    validate_pos,
)


def test_validate_cs_tag_normal_cases():
    try:
        validate_cs_tag("=ACGT*ag+cc-tt~ac12gt")
        validate_cs_tag("=A*ag+c-t~gt1ag")
        validate_cs_tag("=A")
        validate_cs_tag(":1")
        validate_cs_tag("*ag")
        validate_cs_tag("+c")
        validate_cs_tag("-t")
        validate_cs_tag("~ac1gt")
    except ValueError:
        pytest.fail("ValueError was raised but should not have been")


def test_validate_cs_tag_abnormal_cases():
    with pytest.raises(ValueError):
        validate_cs_tag("=ACGT:INVALID")
    with pytest.raises(ValueError):
        validate_cs_tag("=A:")
    with pytest.raises(ValueError):
        validate_cs_tag("*a")
    with pytest.raises(ValueError):
        validate_cs_tag("+")
    with pytest.raises(ValueError):
        validate_cs_tag("-")
    with pytest.raises(ValueError):
        validate_cs_tag("~acgt")


def test_validate_cs_tag_edge_cases():
    try:
        validate_cs_tag("")
    except ValueError:
        pytest.fail("ValueError was raised but should not have been")


def test_validate_short_format():
    # Test with valid cs tags
    try:
        validate_short_format(":123")
        validate_short_format(":123*gt")
    except ValueError:
        pytest.fail("Unexpected ValueError with valid cs tags")

    # Test with invalid cs tags
    with pytest.raises(ValueError):
        validate_short_format("=ACGT")
    with pytest.raises(ValueError):
        validate_short_format("=ACGTN")
    with pytest.raises(ValueError):
        validate_short_format("=N")


def test_validate_long_format():
    # Test with valid cs tags
    try:
        validate_long_format("=ACGT")
        validate_long_format("=AC*gt=T")
        validate_long_format("=C*gt=T")
    except ValueError:
        pytest.fail("Unexpected ValueError with valid cs tags")

    # Test with invalid cs tags
    with pytest.raises(ValueError):
        validate_long_format(":12345")

    # Test with mixed cs tags
    with pytest.raises(ValueError):
        validate_long_format("=ACGT:12345")


def test_validate_threshold():
    # Test with valid thresholds
    try:
        validate_threshold(0)
        validate_threshold(20)
        validate_threshold(40)
    except ValueError:
        pytest.fail("Unexpected ValueError with valid thresholds")

    # Test with invalid type
    with pytest.raises(ValueError):
        validate_threshold("string")
    with pytest.raises(ValueError):
        validate_threshold(3.5)

    # Test with out-of-range thresholds
    with pytest.raises(ValueError):
        validate_threshold(-1)
    with pytest.raises(ValueError):
        validate_threshold(41)


def test_validate_pos():
    validate_pos(1)
    validate_pos(5)
    validate_pos(100)

    with pytest.raises(ValueError, match=r"pos must be a positive integer, but got 0"):
        validate_pos(0)

    with pytest.raises(ValueError, match=r"pos must be a positive integer, but got -1"):
        validate_pos(-1)
