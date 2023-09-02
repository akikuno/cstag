import pytest
from src.cstag.split import split


@pytest.mark.parametrize(
    "input_str, prefix, expected_output",
    [
        # Test for empty string
        ("", False, []),
        # Test for no operators
        ("cs:Z:", False, []),
        # prefix=True
        ("cs:Z:", True, ["cs:Z:"]),
        # Tests for short form
        (":4", False, [":4"]),
        (":4:3", False, [":4", ":3"]),
        (":4*ag:3", False, [":4", "*ag", ":3"]),
        (":4+ag:3", False, [":4", "+ag", ":3"]),
        (":4-ag:3", False, [":4", "-ag", ":3"]),
        (":4~gt1ac:3", False, [":4", "~gt1ac", ":3"]),
        (":2*ag+t-ccc~gt1ac:2", False, [":2", "*ag", "+t", "-ccc", "~gt1ac", ":2"]),
        # Tests for long form
        ("=ACGT", False, ["=ACGT"]),
        ("=ACGT=CGTA", False, ["=ACGT", "=CGTA"]),
        ("=ACGT*ag=CGT", False, ["=ACGT", "*ag", "=CGT"]),
        ("=ACGT+ag=CGT", False, ["=ACGT", "+ag", "=CGT"]),
        ("=ACGT-ag=CGT", False, ["=ACGT", "-ag", "=CGT"]),
        ("=ACGT~gt1ac=CGT", False, ["=ACGT", "~gt1ac", "=CGT"]),
        ("=AC*ag+t-ccc~gt1ac=AC", False, ["=AC", "*ag", "+t", "-ccc", "~gt1ac", "=AC"]),
    ],
)
def test_split(input_str, prefix, expected_output):
    assert split(input_str, prefix) == expected_output
