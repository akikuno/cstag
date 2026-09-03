import pytest

from cstag.utils.validator import (
    validate_cs_tag,
    validate_long_format,
    validate_pos,
    validate_short_format,
    validate_threshold,
)


def test_validate_cs_tag_normal_cases():
    validate_cs_tag("=ACGT*ag+cc-tt~ac12gt")
    validate_cs_tag("=A*ag+c-t~gt1ag")
    validate_cs_tag("=A")
    validate_cs_tag(":1")
    validate_cs_tag("*ag")
    validate_cs_tag("+c")
    validate_cs_tag("-t")
    validate_cs_tag("~ac1gt")


def test_validate_cs_tag_abnormal_cases():
    for cs_tag in ("=ACGT:INVALID", "=A:", "*a", "+", "-", "~acgt"):
        with pytest.raises(ValueError, match="Invalid cs tag"):
            validate_cs_tag(cs_tag)


def test_validate_cs_tag_edge_cases():
    validate_cs_tag("")


def test_validate_short_format():
    # Test with valid cs tags
    validate_short_format(":123")
    validate_short_format(":123*gt")

    # Test with invalid cs tags
    for cs_tag in ("=ACGT", "=ACGTN", "=N"):
        with pytest.raises(ValueError, match="cs tag must be in short format"):
            validate_short_format(cs_tag)


def test_validate_long_format():
    # Test with valid cs tags
    validate_long_format("=ACGT")
    validate_long_format("=AC*gt=T")
    validate_long_format("=C*gt=T")

    # Test with invalid cs tags
    with pytest.raises(ValueError, match="cs tag must be in long format"):
        validate_long_format(":12345")

    # Test with mixed cs tags
    with pytest.raises(ValueError, match="cs tag must be in long format"):
        validate_long_format("=ACGT:12345")


def test_validate_threshold():
    # Test with valid thresholds
    validate_threshold(0)
    validate_threshold(20)
    validate_threshold(40)

    # Test with invalid type
    for threshold in ("string", 3.5):
        with pytest.raises(ValueError, match="threshold must be an integer"):
            validate_threshold(threshold)

    # Test with out-of-range thresholds
    for threshold in (-1, 41):
        with pytest.raises(
            ValueError,
            match="threshold must be within a range between 0 to 40",
        ):
            validate_threshold(threshold)


def test_validate_pos():
    validate_pos(1)
    validate_pos(5)
    validate_pos(100)

    with pytest.raises(ValueError, match=r"pos must be a positive integer, but got 0"):
        validate_pos(0)

    with pytest.raises(ValueError, match=r"pos must be a positive integer, but got -1"):
        validate_pos(-1)
