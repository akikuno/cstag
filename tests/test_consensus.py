from collections import deque
from src.cstag.consensus import (
    split_cs_tags,
    normalize_read_lengths,
    get_consensus,
    consensus,
)


def test_split_cs_tags():
    # Test with a variety of cs tags
    cs_tags = ["=ACGT", "=AC*gt=T", "=C~gt10ag=T", "=ACT+ccc=T"]
    expected_output = [
        deque(["A", "C", "G", "T"]),
        deque(["A", "C", "*gt", "T"]),
        deque(["C", "~gt10ag", "T"]),
        deque(["A", "C", "T+ccc", "T"]),
    ]
    assert split_cs_tags(cs_tags) == expected_output

    # Test with empty cs tag
    assert split_cs_tags([""]) == [deque([])]

    # Test with no cs tags
    assert split_cs_tags([]) == []


def test_normalize_read_lengths():
    # Test with a variety of cs deques and starts
    cs_deques = [deque(["A", "C", "G", "T"]), deque(["A", "C"]), deque(["G", "T"])]
    starts = [0, 2, 4]
    expected_output = [
        deque(["A", "C", "G", "T", "N", "N"]),
        deque(["N", "N", "A", "C", "N", "N"]),
        deque(["N", "N", "N", "N", "G", "T"]),
    ]

    assert normalize_read_lengths(cs_deques, starts) == expected_output


def test_get_consensus():
    # Test with a variety of cs deques
    cs_deques = [deque(["A", "C", "G", "T"]), deque(["A", "C", "G", "T"]), deque(["A", "C", "G", "T"])]
    assert get_consensus(cs_deques) == "=ACGT"

    # Test with different cs tags in the deques
    cs_deques = [deque(["A", "C", "*ga", "T"]), deque(["A", "C", "G", "*tc"]), deque(["A", "C", "*ga", "T"])]
    assert get_consensus(cs_deques) == "=AC*ga=T"

    # Test with empty cs deque
    assert get_consensus([deque([])]) == ""

    # Test with no cs deques
    assert get_consensus([]) == ""

    # Test with multimodal cs tags
    cs_deques = [deque(["A", "C", "G", "T"]), deque(["A", "C", "G", "T"]), deque(["*", "*", "*", "*"])]
    assert get_consensus(cs_deques) == "=ACGT"


###########################################################
# main
###########################################################


def test_substitution():
    CSTAG = [
        "=ACGT",
        "=AC*gt=T",
        "=C*gt=T",
        "=C*gt=T",
        "=ACT+ccc=T",
    ]
    POS = [1, 1, 2, 2, 1]
    assert consensus(CSTAG, POS) == "=AC*gt=T"


def test_insertion():
    CSTAG = ["=ACGT", "=AC+ggggg=GT", "=C+ggggg=GT", "=C+ggggg=GT"]
    POS = [1, 1, 2, 2]
    assert consensus(CSTAG, POS) == "=NC+ggggg=GT"


def test_deletion():
    CSTAG = ["=ACGT", "=AC-ggggg=GT", "=C-ggggg=GT", "=C-ggggg=GT"]
    POS = [1, 1, 2, 2]
    assert consensus(CSTAG, POS) == "=NC-ggggg=GT"


def test_positions():
    CSTAG = ["=ACGT", "=CGT", "=GT"]
    POS = [1, 2, 3]
    assert consensus(CSTAG, POS) == "=NCGT"


def test_splicing():
    CSTAG = [
        "=ACGT",
        "=AC~gc100ag=T",
        "=C~gc100ag=T",
        "=C~gc100ag=T",
    ]
    POS = [1, 1, 2, 2]
    assert consensus(CSTAG, POS) == "=NC~gc100ag=T"
