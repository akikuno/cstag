from collections import deque
from src.cstag.consensus import (
    extract_softclips,
    calculate_read_starts,
    split_cs_tags,
    normalize_read_lengths,
    get_consensus,
    consensus,
)


def test_extract_softclips():
    # Test with a variety of CIGAR strings
    cigar_strings = ["4S3M", "3M4S", "10M", "5S5M5S", "5M"]
    expected_output = [4, 0, 0, 5, 0]

    assert extract_softclips(cigar_strings) == expected_output

    # Test with empty CIGAR string
    assert extract_softclips([""]) == [0]

    # Test with no CIGAR strings
    assert extract_softclips([]) == []


def test_calculate_read_starts():
    # Test with a variety of POS and CIGAR strings
    POS = [6, 8, 10]
    CIGAR = ["4S3M", "3M", "3S2M"]
    expected_output = [0 + 4, 2 + 0, 4 + 3]

    assert calculate_read_starts(POS, CIGAR) == expected_output


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
    CIGAR = ["4M", "4M", "1S3M", "3M", "3M3I1M"]
    POS = [1, 1, 1, 2, 1]
    assert consensus(CSTAG, CIGAR, POS) == "=AC*gt=T"


def test_insertion():
    CSTAG = ["=ACGT", "=AC+ggggg=GT", "=C+ggggg=GT", "=C+ggggg=GT"]
    CIGAR = ["4M", "2M5I1M", "1S5I3M", "1M5I1M"]
    POS = [1, 1, 1, 2]
    assert consensus(CSTAG, CIGAR, POS) == "=NC+ggggg=GT"


def test_deletion():
    CSTAG = ["=ACGT", "=AC-ggggg=GT", "=C-ggggg=GT", "=C-ggggg=GT"]
    CIGAR = ["4M", "2M5D1M", "1S5D3M", "1M5D1M"]
    POS = [1, 1, 1, 2]
    assert consensus(CSTAG, CIGAR, POS) == "=NC-ggggg=GT"


def test_softclip():
    CSTAG = ["=ACGT", "=CGT", "=GT"]
    CIGAR = ["4M", "1S3M", "2S2M"]
    POS = [1, 1, 1]
    assert consensus(CSTAG, CIGAR, POS) == "=NCGT"


def test_splicing():
    CSTAG = [
        "=ACGT",
        "=AC~gc100ag=T",
        "=C~gc100ag=T",
        "=C~gc100ag=T",
    ]
    CIGAR = ["4M", "2M100N1M", "1S100N3M", "1M100N1M"]
    POS = [1, 1, 1, 2]
    assert consensus(CSTAG, CIGAR, POS) == "=NC~gc100ag=T"
