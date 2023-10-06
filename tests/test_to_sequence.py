from src.cstag import to_sequence


def test_to_sequence_normal_cases():
    assert to_sequence("cs:Z:=ACGT") == "ACGT"
    assert to_sequence("cs:Z:=A+c*cg=T") == "ACGT"
    assert to_sequence("cs:Z:=A+cgt") == "ACGT"
    assert to_sequence("cs:Z:=AC-tt=GT") == "ACGT"
    assert to_sequence("cs:Z:=AC~gt10ag=GT") == "ACGT"
    assert to_sequence("=AC*gt=T-gg=C+tt=A") == "ACTTCTTA"


def test_to_sequence_edge_cases():
    assert to_sequence("") == ""
    assert to_sequence("cs:Z:") == ""
    assert to_sequence("cs:Z:=A") == "A"
    assert to_sequence("cs:Z:+a") == "A"
    assert to_sequence("cs:Z:*ag") == "G"
    assert to_sequence("cs:Z:~gt10ag") == ""
