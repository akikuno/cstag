import pytest
from src.cstag.utils.validator import validate_short_format, validate_long_format, validate_threshold


def test_validate_short_format():
    # Test with valid cs tags
    try:
        validate_short_format(":A")
        validate_short_format(":123")
        validate_short_format(":*")
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
