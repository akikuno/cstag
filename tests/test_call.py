import pytest
from src.cstag.call import (
    _split_cigar,
    _split_md,
    _join_cigar,
    trim_clips,
    generate_cslong_md_based,
    align_length,
    call,
)

###########################################################
# Trim soft and hard clips from the CIGAR and sequence
###########################################################


# split_cigarのテスト
@pytest.mark.parametrize(
    "cigar, expected",
    [
        ("5S10M3S", [("S", 5), ("M", 10), ("S", 3)]),
        ("10M", [("M", 10)]),
        ("", []),
        ("5H10M5H", [("H", 5), ("M", 10), ("H", 5)]),
    ],
)
def test_split_cigar(cigar, expected):
    assert _split_cigar(cigar) == expected


@pytest.mark.parametrize(
    "md_input,expected_output",
    [
        ("6^ATA14A3", [("=", 6), ("^ATA", 3), ("=", 14), ("A", 1), ("=", 3)]),  # Basic Test
        ("", []),  # Empty string
        ("10", [("=", 10)]),  # Only matches
        ("^ACGT", [("^ACGT", 4)]),  # Only deletions
        ("AGCT", [("A", 1), ("G", 1), ("C", 1), ("T", 1)]),  # Only mismatches
        ("5^AC5T2", [("=", 5), ("^AC", 2), ("=", 5), ("T", 1), ("=", 2)]),  # Mixed Cases
        ("1A1^T1", [("=", 1), ("A", 1), ("=", 1), ("^T", 1), ("=", 1)]),  # Mixed Cases
        ("100", [("=", 100)]),  # Large Numbers
        ("^ACGTACGT", [("^ACGTACGT", 8)]),  # No Matches
        ("1ATGC1", [("=", 1), ("A", 1), ("T", 1), ("G", 1), ("C", 1), ("=", 1)]),  # Multiple adjacent mismatches
    ],
)
def test_split_md(md_input, expected_output):
    assert _split_md(md_input) == expected_output


# join_cigarのテスト
@pytest.mark.parametrize(
    "cigar_tuples, expected",
    [
        ([("H", 5), ("M", 10), ("S", 5)], "5H10M5S"),
        ([("M", 10)], "10M"),
        ([], ""),
        ([("H", 5), ("M", 10), ("H", 5)], "5H10M5H"),
        ([("S", 5), ("M", 10)], "5S10M"),
        ([("M", 10), ("S", 5)], "10M5S"),
        ([("H", 5), ("M", 10), ("S", 5)], "5H10M5S"),
        ([("S", 5), ("M", 10), ("H", 5)], "5S10M5H"),
    ],
)
def test_join_cigar(cigar_tuples, expected):
    assert _join_cigar(cigar_tuples) == expected


# trim_clipsのテスト
@pytest.mark.parametrize(
    "cigar, seq, expected_cigar, expected_seq",
    [
        ("5S10M3S", "AAAAATTTTTGGGGGCCC", "10M", "TTTTTGGGGG"),
        ("10M", "TTTTTTTTTT", "10M", "TTTTTTTTTT"),
        ("5H10M5H", "TTTTTTTTTT", "10M", "TTTTTTTTTT"),
        ("5S10M", "AAAAATTTTTTTTTT", "10M", "TTTTTTTTTT"),
        ("10M3S", "TTTTTTTTTTGGG", "10M", "TTTTTTTTTT"),
        ("5S10M5H", "AAAAATTTTTTTTTT", "10M", "TTTTTTTTTT"),
        ("5H10M5S", "TTTTTTTTTTGGGGG", "10M", "TTTTTTTTTT"),
    ],
)
def test_trim_clips(cigar, seq, expected_cigar, expected_seq):
    new_cigar, new_seq = trim_clips(cigar, seq)
    assert new_cigar == expected_cigar
    assert new_seq == expected_seq


###########################################################


###########################################################
# Test cases
def test_generate_cslong_md_based():
    assert generate_cslong_md_based("ACGTACGT", "8") == ["=ACGTACGT"]
    assert generate_cslong_md_based("ACGTACGT", "4^TACG4") == ["=ACGT", "-tacg", "=ACGT"]
    assert generate_cslong_md_based("ACGTACGT", "3A1T2") == ["=ACG", "*at", "=A", "*tc", "=GT"]
    assert generate_cslong_md_based("ACGTACGT", "2^TA4T1") == ["=AC", "-ta", "=GTAC", "*tg", "=T"]
    assert generate_cslong_md_based("ACGTA", "2^TA1G1") == ["=AC", "-ta", "=G", "*gt", "=A"]
    assert generate_cslong_md_based("ACGTAA", "1A1^T1G1") == ["=A", "*ac", "=G", "-t", "=T", "*ga", "=A"]


def test_align_length():
    assert align_length(["=ACGT", "*ta", "=ACGT"]) == "ACGTwACGT"
    assert align_length(["=ACGT", "-atcg", "=ACGT"]) == "ACGTatcgACGT"
    assert align_length(["=ACGT", "*ta", "*gt"]) == "ACGTwk"
    assert align_length(["=AC", "-at", "=GT", "*tc", "=AT"]) == "ACatGTsAT"
    assert align_length(["=A", "*tc", "-t", "=G", "*tg", "=T"]) == "AstGoT"


###########################################################
# main
###########################################################


@pytest.mark.parametrize(
    "cigar, md, seq, expected",
    [
        ("8M2D4M2I", "8^AG6", "ACGTACGTACGTAC", "cs:Z:=ACGTACGT-ag=ACGT+ac"),
        ("5M", "5", "ACGTA", "cs:Z:=ACGTA"),
        ("5M", "3C1", "ACGTG", "cs:Z:=ACG*ct=G"),
        ("5M1I3M", "9", "ACGTAGCTA", "cs:Z:=ACGTA+g=CTA"),
        ("5M1D4M", "5^A4", "ACGTGGCTA", "cs:Z:=ACGTG-a=GCTA"),
        ("3M1D1M1D4M", "3^C1^A4", "ACGGCTAG", "cs:Z:=ACG-c=G-a=CTAG"),
    ],
)
def test_generate_cs_tag_long_form(cigar, md, seq, expected):
    result = call(cigar, md, seq, is_short_form=False)
    assert result == expected


@pytest.mark.parametrize(
    "cigar, md, seq, expected",
    [
        ("8M2D4M2I", "8^AG6", "ACGTACGTACGTAC", "cs:Z::8-ag:4+ac"),
        ("5M", "5", "ACGTA", "cs:Z::5"),
        ("5M", "3C1", "ACGTG", "cs:Z::3*ct:1"),
        ("5M1I3M", "9", "ACGTAGCTA", "cs:Z::5+g:3"),
        ("5M1D4M", "5^A4", "ACGTGGCTA", "cs:Z::5-a:4"),
        ("3M1D1M1D4M", "3^C1^A4", "ACGGCTAG", "cs:Z::3-c:1-a:4"),
    ],
)
def test_generate_cs_tag_short_form(cigar, md, seq, expected):
    result = call(cigar, md, seq, is_short_form=True)
    assert result == expected
