from src.calcs.trim import get_softclip_lengths

cigar = "150S10M10S"


def test_func():
    assert get_softclip_lengths(cigar) == (150, 10)
