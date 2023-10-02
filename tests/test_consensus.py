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
        (["A", "C", "G", "T"]),
        (["A", "C", "*gt", "T"]),
        (["C", "~gt10ag", "T"]),
        (["A", "C", "T+ccc", "T"]),
    ]
    assert split_cs_tags(cs_tags) == expected_output

    # Test with empty cs tag
    assert split_cs_tags([""]) == [([])]

    # Test with no cs tags
    assert split_cs_tags([]) == []


def test_normalize_read_lengths():
    # Test with a variety of cs and starts
    # cs_tags = [(["A", "C", "G", "T"]), (["A", "C"]), (["G", "T"])]
    cs_tags = ["=ACGT", "=AC", "=GT"]
    starts = [0, 2, 4]
    expected_output = [
        (["A", "C", "G", "T", None, None]),
        ([None, None, "A", "C", None, None]),
        ([None, None, None, None, "G", "T"]),
    ]

    assert normalize_read_lengths(cs_tags, starts) == expected_output


def test_get_consensus():
    # Test with a variety of cs
    cs_tags = [(["A", "C", "G", "T"]), (["A", "C", "G", "T"]), (["A", "C", "G", "T"])]
    assert get_consensus(cs_tags) == "=ACGT"

    # Test with different cs tags
    cs_tags = [(["A", "C", "*ga", "T"]), (["A", "C", "G", "*tc"]), (["A", "C", "*ga", "T"])]
    assert get_consensus(cs_tags) == "=AC*ga=T"

    # Test with empty cs
    assert get_consensus([([])]) == ""

    # Test with no cs
    assert get_consensus([]) == ""

    # Test with multimodal cs tags
    cs_tags = [(["A", "C", "G", "T"]), (["A", "C", "G", "T"]), (["*", "*", "*", "*"])]
    assert get_consensus(cs_tags) == "=ACGT"


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
    assert consensus(CSTAG, POS) == "=AC+ggggg=GT"


def test_deletion():
    CSTAG = ["=ACGT", "=AC-ggggg=GT", "=C-ggggg=GT", "=C-ggggg=GT"]
    POS = [1, 1, 2, 2]
    assert consensus(CSTAG, POS) == "=AC-ggggg=GT"


def test_splicing():
    CSTAG = [
        "=ACGT",
        "=AC~gc100ag=T",
        "=C~gc100ag=T",
        "=C~gc100ag=T",
    ]
    POS = [1, 1, 2, 2]
    assert consensus(CSTAG, POS) == "=AC~gc100ag=T"


def test_positions():
    CSTAG = ["=ACGT", "=CGT", "=GT"]
    POS = [1, 2, 3]
    assert consensus(CSTAG, POS) == "=ACGT"


def test_positions_more_than_one():
    CSTAG = [
        "=ACGT",
        "=AC*gt=T",
        "=C*gt=T",
        "=C*gt=T",
        "=ACT+ccc=T",
    ]
    POS = [101, 101, 102, 102, 101]
    assert consensus(CSTAG, POS) == "=AC*gt=T"
