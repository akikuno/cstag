import pytest
from src.cstag.split import split


@pytest.mark.parametrize(
    "input_str, expected_output",
    [
        # Test for empty string
        ("", []),
        # Test for no operators
        ("cs:Z:", ["cs:Z:"]),
        # Tests for short form
        ("cs:Z::4", ["cs:Z:", ":4"]),
        ("cs:Z::4:3", ["cs:Z:", ":4", ":3"]),
        ("cs:Z::4*ag:3", ["cs:Z:", ":4", "*ag", ":3"]),
        ("cs:Z::4+ag:3", ["cs:Z:", ":4", "+ag", ":3"]),
        ("cs:Z::4-ag:3", ["cs:Z:", ":4", "-ag", ":3"]),
        ("cs:Z::4~gt1ac:3", ["cs:Z:", ":4", "~gt1ac", ":3"]),
        ("cs:Z::2*ag+t-ccc~gt1ac:2", ["cs:Z:", ":2", "*ag", "+t", "-ccc", "~gt1ac", ":2"]),
        # Tests for long form
        ("cs:Z:=ACGT", ["cs:Z:", "=ACGT"]),
        ("cs:Z:=ACGT=CGTA", ["cs:Z:", "=ACGT", "=CGTA"]),
        ("cs:Z:=ACGT*ag=CGT", ["cs:Z:", "=ACGT", "*ag", "=CGT"]),
        ("cs:Z:=ACGT+ag=CGT", ["cs:Z:", "=ACGT", "+ag", "=CGT"]),
        ("cs:Z:=ACGT-ag=CGT", ["cs:Z:", "=ACGT", "-ag", "=CGT"]),
        ("cs:Z:=ACGT~gt1ac=CGT", ["cs:Z:", "=ACGT", "~gt1ac", "=CGT"]),
        ("cs:Z:=AC*ag+t-ccc~gt1ac=AC", ["cs:Z:", "=AC", "*ag", "+t", "-ccc", "~gt1ac", "=AC"]),
    ],
)
def test_split(input_str, expected_output):
    assert split(input_str) == expected_output
