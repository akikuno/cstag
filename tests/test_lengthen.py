import re
from src.cstag import lengthen


def test_softclip():
    SEQ = "ATACTTAATTATACATTTGAAACGCGCCCAAGTGACGCTAGGCAAGTCAGAGCAGGTTCCCGTGTTAGCTTAAGGGTAAACATACAAGTC"
    CSTAG = "cs:Z::90"
    cslong = "cs:Z:=ATACTTAATTATACATTTGAAACGCGCCCAAGTGACGCTAGGCAAGTCAGAGCAGGTTCCCGTGTTAGCTTAAGGGTAAACATACAAGTC"
    CIGAR = "90M"
    assert lengthen(CSTAG, CIGAR, SEQ) == cslong


def test_substitution():
    SEQ = "ACTGTGCGGCATACTTAATTATACATTTGAAACGCGCCCAAGTGACGCTGGGCAAGTCAGAGCAGGTTCCCGTGTTAGCTTAAGGGTAAACATACAAGTC"
    CSTAG = "cs:Z::49*ag:50"
    CIGAR = "100M"
    cslong = (
        "cs:Z:=ACTGTGCGGCATACTTAATTATACATTTGAAACGCGCCCAAGTGACGCT*ag=GGCAAGTCAGAGCAGGTTCCCGTGTTAGCTTAAGGGTAAACATACAAGTC"
    )
    assert lengthen(CSTAG, CIGAR, SEQ) == cslong


def test_deletion():
    SEQ = "ACTGTGCGGCATACTTAATTATACATTTGAAACGCGCCCAGGCAAGTCAGAGCAGGTTCCCGTGTTAGCTTAAGGGTAAACATACAAGTC"
    CSTAG = "cs:Z::39-aagtgacgct:51"
    CIGAR = "39M10D51M"
    cslong = (
        "cs:Z:=ACTGTGCGGCATACTTAATTATACATTTGAAACGCGCCC-aagtgacgct=AGGCAAGTCAGAGCAGGTTCCCGTGTTAGCTTAAGGGTAAACATACAAGTC"
    )
    assert lengthen(CSTAG, CIGAR, SEQ) == cslong


def test_insertion():
    SEQ = (
        "ACTGTGCGGCATACTTAATTATACATTTGAAACGCGCCCAAGTGACGCTCCCCCCCCCCAGGCAAGTCAGAGCAGGTTCCCGTGTTAGCTTAAGGGTAAACATACAAGTC"
    )
    CSTAG = "cs:Z::49+cccccccccc:51"
    CIGAR = "49M10I51M"
    cslong = "cs:Z:=ACTGTGCGGCATACTTAATTATACATTTGAAACGCGCCCAAGTGACGCT+cccccccccc=AGGCAAGTCAGAGCAGGTTCCCGTGTTAGCTTAAGGGTAAACATACAAGTC"
    assert lengthen(CSTAG, CIGAR, SEQ) == cslong


def test_splicing():
    SEQ = "GTAGGTTGTGAGATGCGGGAGAGGTTCTCGATCTTCCCGTGGGACGTCAACCTTTCCCTTGATAAAGCATCCCGCTCGGGTATGGCAGTGAGTACGCCTTCTGAATTGTGCTATCCTTCGTCCTTATCAAAGCTTGCTACCAATAATTAGGATTATTGCCTTGCGACAGACTTCCTACTCACACTCCCTCACATTGAGCTACTCGATGGGCGATTAGCTTGACCCGCTCTGTAGGGTCGCGACTACGTGACTAAGAGTAGGCCGGGAGTGTAGACCTTTGGGGTTGAATAAATCTATTGTACTAATCGGCTTCAACGAGCCGTACAGGTGGCACCTCAGGAGGGGCCCGCAGGGAGGAAGTAAACTGCTATTCGTCGCCGTTGGTGGTAACTAATTGTGTTCCTTGCCACTACAATTGTATCTAAGCCGTGTAATGAGAACAACCACACCTTAGCGAATTGATGCGCCGCTTCGGAATACCGTTTTGGCTACCCGTTAC"
    CSTAG = "cs:Z::250~gc1001ag:249"
    CIGAR = "250M1001N249M"
    cslong = "cs:Z:=GTAGGTTGTGAGATGCGGGAGAGGTTCTCGATCTTCCCGTGGGACGTCAACCTTTCCCTTGATAAAGCATCCCGCTCGGGTATGGCAGTGAGTACGCCTTCTGAATTGTGCTATCCTTCGTCCTTATCAAAGCTTGCTACCAATAATTAGGATTATTGCCTTGCGACAGACTTCCTACTCACACTCCCTCACATTGAGCTACTCGATGGGCGATTAGCTTGACCCGCTCTGTAGGGTCGCGACTACGTGA~gc1001ag=CTAAGAGTAGGCCGGGAGTGTAGACCTTTGGGGTTGAATAAATCTATTGTACTAATCGGCTTCAACGAGCCGTACAGGTGGCACCTCAGGAGGGGCCCGCAGGGAGGAAGTAAACTGCTATTCGTCGCCGTTGGTGGTAACTAATTGTGTTCCTTGCCACTACAATTGTATCTAAGCCGTGTAATGAGAACAACCACACCTTAGCGAATTGATGCGCCGCTTCGGAATACCGTTTTGGCTACCCGTTAC"
    assert lengthen(CSTAG, CIGAR, SEQ) == cslong


def test_5bpIns_3bp_Del():
    SEQ = "ACTGTGCGGCATACTTAATGGGGGTATACATTTGAAACGCGCCCTGACGCTAGGCAAGTCAGAGCAGGTTCCCGTGTTAGCTTAAGGGTAAACATACAAGTC"
    CSTAG = "cs:Z::19+ggggg:20-aag:58"
    CIGAR = "19M5I20M3D58M"
    cslong = "cs:Z:=ACTGTGCGGCATACTTAAT+ggggg=TATACATTTGAAACGCGCCC-aag=TGACGCTAGGCAAGTCAGAGCAGGTTCCCGTGTTAGCTTAAGGGTAAACATACAAGTC"
    assert lengthen(CSTAG, CIGAR, SEQ) == cslong


def test_first_5nt_del_softclip_5nt():
    SEQ = "TTTTTGCGGCATACTTAATTATACATTTGAAACGCGCCCAAGTGACGCTAGGCAAGTCAGAGCAGGTTCCCGTGTTAGCTTAAGGGTAAACATACAAGTC"
    CSTAG = "cs:Z::96"
    CIGAR = "4S96M"
    cslong = "cs:Z:=TGCGGCATACTTAATTATACATTTGAAACGCGCCCAAGTGACGCTAGGCAAGTCAGAGCAGGTTCCCGTGTTAGCTTAAGGGTAAACATACAAGTC"
    assert lengthen(CSTAG, CIGAR, SEQ) == cslong


def test_softclip_plus_5nt():
    CSTAG = "cs:Z::100"
    SEQ = "TTTTTACTGTGCGGCATACTTAATTATACATTTGAAACGCGCCCAAGTGACGCTAGGCAAGTCAGAGCAGGTTCCCGTGTTAGCTTAAGGGTAAACATACAAGTC"
    CIGAR = "5S100M"
    cslong = (
        "cs:Z:=ACTGTGCGGCATACTTAATTATACATTTGAAACGCGCCCAAGTGACGCTAGGCAAGTCAGAGCAGGTTCCCGTGTTAGCTTAAGGGTAAACATACAAGTC"
    )
    assert lengthen(CSTAG, CIGAR, SEQ) == cslong


def test_softclip_plusminus_10nt():
    CSTAG = "cs:Z::100"
    SEQ = (
        "TTTTTACTGTGCGGCATACTTAATTATACATTTGAAACGCGCCCAAGTGACGCTAGGCAAGTCAGAGCAGGTTCCCGTGTTAGCTTAAGGGTAAACATACAAGTCTTTTT"
    )
    CIGAR = "5S100M5S"
    cslong = (
        "cs:Z:=ACTGTGCGGCATACTTAATTATACATTTGAAACGCGCCCAAGTGACGCTAGGCAAGTCAGAGCAGGTTCCCGTGTTAGCTTAAGGGTAAACATACAAGTC"
    )
    assert lengthen(CSTAG, CIGAR, SEQ) == cslong


def test_real():
    def call_cs_cigar_seq(content):
        names = [
            "QNAME",
            "FLAG",
            "RNAME",
            "POS",
            "MAPQ",
            "CIGAR",
            "RNEXT",
            "PNEXT",
            "TLEN",
            "SEQ",
            "QUAL",
        ]
        content_dict = {n: c for n, c in zip(names, content.split("\t"))}
        content_dict.update({"CS": c for c in content.split("\t") if re.search(r"^cs:Z", c)})
        return content_dict["CS"], content_dict["CIGAR"], content_dict["SEQ"]

    with open("tests/data/real/tyr_cs.sam") as f:
        sam_short = [x.strip() for x in f.readlines()]
    contents_short = [s for s in sam_short if not re.search(r"^@", s)]

    cs_lengthened = []
    for content in contents_short:
        cs, cigar, seq = call_cs_cigar_seq(content)
        cs_lengthened.append(lengthen(cs, cigar, seq))

    with open("tests/data/real/tyr_cslong.sam") as f:
        sam_long = [x.strip() for x in f.readlines()]
    contents_long = [s for s in sam_long if not re.search(r"^@", s)]

    cs_long = []
    for content in contents_long:
        cs, cigar, seq = call_cs_cigar_seq(content)
        cs_long.append(cs)

    for i in range(len(cs_lengthened)):
        assert cs_lengthened[i] == cs_long[i]
