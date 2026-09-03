import pytest

import cstag
from cstag.consensus import (
    consensus,
    get_consensus,
    normalize_read_lengths,
    split_cs_tags,
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
    cs_tags = [
        (["A", "C", "*ga", "T"]),
        (["A", "C", "G", "*tc"]),
        (["A", "C", "*ga", "T"]),
    ]
    assert get_consensus(cs_tags) == "=AC*ga=T"

    # Test with empty cs
    assert get_consensus([([])]) == ""

    # Test with no cs
    assert get_consensus([]) == ""

    # Test with multimodal cs tags
    cs_tags = [(["A", "C", "G", "T"]), (["A", "C", "G", "T"]), (["*", "*", "*", "*"])]
    assert get_consensus(cs_tags) == "=ACGT"


def test_get_consensus_selects_one_mutation_from_a_multimodal_position():
    cs_tags = [(["A"]), (["*ag"]), (["*at"])]
    assert get_consensus(cs_tags) == "*ag"

    insertion_tie = [(["A"]), (["A+g"])]
    assert get_consensus(insertion_tie) == "=A+g"


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
    CSTAG = ["=ACGT", "=AC+acgt=GT", "=C+acgt=GT", "=C+acgt=GT"]
    POS = [1, 1, 2, 2]
    assert consensus(CSTAG, POS) == "=AC+acgt=GT"


def test_deletion():
    CSTAG = ["=ACGT", "=AC-acgt=GT", "=C-acgt=GT", "=C-acgt=GT"]
    POS = [1, 1, 2, 2]
    assert consensus(CSTAG, POS) == "=AC-acgt=GT"


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


def test_consensus_default_api_and_prefix_remain_strings():
    assert cstag.consensus(["=ACGT"], [1]) == "=ACGT"
    assert cstag.consensus(["=ACGT"], [1], prefix=True) == "cs:Z:=ACGT"


def test_consensus_quality_passes_at_exact_agreement_threshold():
    cs_tags = ["=ACGT", "=ACGT", "=ACGT", "=AC*gt=T"]
    positions = [1, 1, 1, 1]

    assert consensus(cs_tags, positions, min_agreement=0.75) == {
        "consensus": "=ACGT",
        "passed": True,
        "agreement": 0.75,
        "max_edit_distance": 1,
    }


def test_consensus_quality_failure_keeps_candidate_and_metrics():
    cs_tags = ["=ACGT", "=ACGT", "=ACGT", "=AC*gt=T"]
    positions = [1, 1, 1, 1]

    assert consensus(cs_tags, positions, min_agreement=0.7501) == {
        "consensus": "=ACGT",
        "passed": False,
        "agreement": 0.75,
        "max_edit_distance": 1,
    }


def test_consensus_quality_can_be_reported_without_a_threshold():
    assert consensus(["=ACGT"], [1], prefix=True, return_result=True) == {
        "consensus": "cs:Z:=ACGT",
        "passed": True,
        "agreement": 1.0,
        "max_edit_distance": 0,
    }


def test_consensus_agreement_uses_covered_reads_at_each_position():
    assert consensus(["=ACGT", "=CG"], [1, 2], return_result=True) == {
        "consensus": "=ACGT",
        "passed": True,
        "agreement": 1.0,
        "max_edit_distance": 0,
    }


@pytest.mark.parametrize(
    ("variant_tag", "expected_distance"),
    [
        ("=AC*gt=T", 1),
        ("=AC+gg=GT", 2),
        ("=A-cg=T", 2),
        ("=A~cg2gt=T", 2),
    ],
)
def test_consensus_quality_handles_each_variant_class(variant_tag, expected_distance):
    result = consensus(
        ["=ACGT", "=ACGT", "=ACGT", variant_tag],
        [1, 1, 1, 1],
        min_agreement=0.75,
    )

    assert result == {
        "consensus": "=ACGT",
        "passed": True,
        "agreement": 0.75,
        "max_edit_distance": expected_distance,
    }


def test_max_edit_distance_is_the_largest_nearest_neighbor_distance():
    result = consensus(
        ["=AAAA", "=AAA*at", "*at*at*at*at"],
        [1, 1, 1],
        return_result=True,
    )

    assert result["max_edit_distance"] == 3


def test_max_edit_distance_ignores_non_overlapping_read_ends():
    result = consensus(["=ACGT", "=CG"], [1, 2], return_result=True)
    assert result["max_edit_distance"] == 0


def test_max_edit_distance_is_none_when_a_read_has_no_overlapping_neighbor():
    assert consensus(["=A", "=T"], [1, 2], return_result=True) == {
        "consensus": "=AT",
        "passed": True,
        "agreement": 1.0,
        "max_edit_distance": None,
    }


@pytest.mark.parametrize(
    "min_agreement", [-0.01, 1.01, float("nan"), float("inf"), -float("inf")]
)
def test_invalid_min_agreement_values_raise_value_error(min_agreement):
    with pytest.raises(ValueError, match="finite number between 0 and 1"):
        consensus(["=ACGT"], [1], min_agreement=min_agreement)


@pytest.mark.parametrize("min_agreement", [True, False, "0.75", object()])
def test_invalid_min_agreement_types_raise_type_error(min_agreement):
    with pytest.raises(TypeError, match="real number"):
        consensus(["=ACGT"], [1], min_agreement=min_agreement)
