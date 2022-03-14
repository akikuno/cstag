from src.cstag.cstag import lengthen

def test_softclip():
    seq = "ATACTTAATTATACATTTGAAACGCGCCCAAGTGACGCTAGGCAAGTCAGAGCAGGTTCCCGTGTTAGCTTAAGGGTAAACATACAAGTC"
    cstag = "cs:Z::90"
    cslong = "cs:Z:=ATACTTAATTATACATTTGAAACGCGCCCAAGTGACGCTAGGCAAGTCAGAGCAGGTTCCCGTGTTAGCTTAAGGGTAAACATACAAGTC"
    assert lengthen(cstag, seq) == cslong


def test_substitution():
    seq = "ACTGTGCGGCATACTTAATTATACATTTGAAACGCGCCCAAGTGACGCTGGGCAAGTCAGAGCAGGTTCCCGTGTTAGCTTAAGGGTAAACATACAAGTC"
    cstag = "cs:Z::49*ag:50"
    cslong = "cs:Z:=ACTGTGCGGCATACTTAATTATACATTTGAAACGCGCCCAAGTGACGCT*ag=GGCAAGTCAGAGCAGGTTCCCGTGTTAGCTTAAGGGTAAACATACAAGTC"
    assert lengthen(cstag, seq) == cslong

def test_deletion():
    seq = "ACTGTGCGGCATACTTAATTATACATTTGAAACGCGCCCAGGCAAGTCAGAGCAGGTTCCCGTGTTAGCTTAAGGGTAAACATACAAGTC"
    cstag = "cs:Z::39-aagtgacgct:51"
    cslong = "cs:Z:=ACTGTGCGGCATACTTAATTATACATTTGAAACGCGCCC-aagtgacgct=AGGCAAGTCAGAGCAGGTTCCCGTGTTAGCTTAAGGGTAAACATACAAGTC"
    assert lengthen(cstag, seq) == cslong

def test_insertion():
    seq = "ACTGTGCGGCATACTTAATTATACATTTGAAACGCGCCCAAGTGACGCTCCCCCCCCCCAGGCAAGTCAGAGCAGGTTCCCGTGTTAGCTTAAGGGTAAACATACAAGTC"
    cstag = "cs:Z::49+cccccccccc:51"
    cslong = "cs:Z:=ACTGTGCGGCATACTTAATTATACATTTGAAACGCGCCCAAGTGACGCT+cccccccccc=AGGCAAGTCAGAGCAGGTTCCCGTGTTAGCTTAAGGGTAAACATACAAGTC"
    assert lengthen(cstag, seq) == cslong

def test_splicing():
    seq = "GTAGGTTGTGAGATGCGGGAGAGGTTCTCGATCTTCCCGTGGGACGTCAACCTTTCCCTTGATAAAGCATCCCGCTCGGGTATGGCAGTGAGTACGCCTTCTGAATTGTGCTATCCTTCGTCCTTATCAAAGCTTGCTACCAATAATTAGGATTATTGCCTTGCGACAGACTTCCTACTCACACTCCCTCACATTGAGCTACTCGATGGGCGATTAGCTTGACCCGCTCTGTAGGGTCGCGACTACGTGACTAAGAGTAGGCCGGGAGTGTAGACCTTTGGGGTTGAATAAATCTATTGTACTAATCGGCTTCAACGAGCCGTACAGGTGGCACCTCAGGAGGGGCCCGCAGGGAGGAAGTAAACTGCTATTCGTCGCCGTTGGTGGTAACTAATTGTGTTCCTTGCCACTACAATTGTATCTAAGCCGTGTAATGAGAACAACCACACCTTAGCGAATTGATGCGCCGCTTCGGAATACCGTTTTGGCTACCCGTTAC"
    cstag = "cs:Z::250~gc1001ag:249"
    cslong = "cs:Z:=GTAGGTTGTGAGATGCGGGAGAGGTTCTCGATCTTCCCGTGGGACGTCAACCTTTCCCTTGATAAAGCATCCCGCTCGGGTATGGCAGTGAGTACGCCTTCTGAATTGTGCTATCCTTCGTCCTTATCAAAGCTTGCTACCAATAATTAGGATTATTGCCTTGCGACAGACTTCCTACTCACACTCCCTCACATTGAGCTACTCGATGGGCGATTAGCTTGACCCGCTCTGTAGGGTCGCGACTACGTGA~gc1001ag=CTAAGAGTAGGCCGGGAGTGTAGACCTTTGGGGTTGAATAAATCTATTGTACTAATCGGCTTCAACGAGCCGTACAGGTGGCACCTCAGGAGGGGCCCGCAGGGAGGAAGTAAACTGCTATTCGTCGCCGTTGGTGGTAACTAATTGTGTTCCTTGCCACTACAATTGTATCTAAGCCGTGTAATGAGAACAACCACACCTTAGCGAATTGATGCGCCGCTTCGGAATACCGTTTTGGCTACCCGTTAC"
    assert lengthen(cstag, seq) == cslong
