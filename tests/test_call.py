import pytest
from src.cstag.call import (
    parse_cigar,
    parse_md,
    join_cigar,
    trim_clips,
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
def testparse_cigar(cigar, expected):
    assert parse_cigar(cigar) == expected


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
def testparse_md(md_input, expected_output):
    assert parse_md(md_input) == expected_output


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
def testjoin_cigar(cigar_tuples, expected):
    assert join_cigar(cigar_tuples) == expected


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
# main
###########################################################


@pytest.mark.parametrize(
    "cigar, md, seq, expected",
    [
        ("8M2D4M2I", "8^AG6", "ACGTACGTACGTAC", "=ACGTACGT-ag=ACGT+ac"),
        ("5M", "5", "ACGTA", "=ACGTA"),
        ("5M", "3C1", "ACGTG", "=ACG*ct=G"),
        ("5M1I3M", "9", "ACGTAGCTA", "=ACGTA+g=CTA"),
        ("5M1D4M", "5^A4", "ACGTGGCTA", "=ACGTG-a=GCTA"),
        ("3M1D1M1D4M", "3^C1^A4", "ACGGCTAG", "=ACG-c=G-a=CTAG"),
        ("3S5M", "5", "NNNACGTA", "=ACGTA"),
        ("8M2D4M2I3N1M", "2A5^AG7", "ACGTACGTACGTACG", "=AC*ag=TACGT-ag=ACGT+ac~nn3nn=G"),
        ("5M", "0C4", "ACGTA", "*ca=CGTA"),
        ("5M", "4C0", "ACGTA", "=ACGT*ca"),
        ("5M", "0C3C0", "ACGTA", "*ca=CGT*ca"),
        ("5M", "0C3C0", "ACGTA", "*ca=CGT*ca"),
        ("5M", "2CC1", "ACGTA", "=AC*cg*ct=A"),
        ("3M2D1M2I1M3N1M", "3^GG0A2", "AAATCCTT", "=AAA-gg*at+cc=T~nn3nn=T"),
    ],
)
def test_generate_cs_tag_long_form(cigar, md, seq, expected):
    result = call(cigar, md, seq, long=True)
    assert result == expected


@pytest.mark.parametrize(
    "cigar, md, seq, expected",
    [
        ("8M2D4M2I", "8^AG6", "ACGTACGTACGTAC", ":8-ag:4+ac"),
        ("5M", "5", "ACGTA", ":5"),
        ("5M", "3C1", "ACGTG", ":3*ct:1"),
        ("5M1I3M", "9", "ACGTAGCTA", ":5+g:3"),
        ("5M1D4M", "5^A4", "ACGTGGCTA", ":5-a:4"),
        ("3M1D1M1D4M", "3^C1^A4", "ACGGCTAG", ":3-c:1-a:4"),
        ("3S5M", "5", "NNNACGTA", ":5"),
        ("8M2D4M2I3N1M", "2A5^AG7", "ACGTACGTACGTACG", ":2*ag:5-ag:4+ac~nn3nn:1"),
        ("5M", "0C3C0", "ACGTA", "*ca:3*ca"),
        ("5M", "2CC1", "ACGTA", ":2*cg*ct:1"),
        ("3M2D1M2I1M3N1M", "3^GG0A2", "AAATCCTT", ":3-gg*at+cc:1~nn3nn:1"),
    ],
)
def test_generate_cs_tag_short_form(cigar, md, seq, expected):
    result = call(cigar, md, seq, long=False)
    assert result == expected
