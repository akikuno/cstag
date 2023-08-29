import re
from src.cstag import shorten


def test_softclip():
    CSTAG = "=ATACTTAATTATACATTTGAAACGCGCCCAAGTGACGCTAGGCAAGTCAGAGCAGGTTCCCGTGTTAGCTTAAGGGTAAACATACAAGTC"

    csshort = ":90"
    assert shorten(CSTAG) == csshort


def test_substitution():
    CSTAG = "=ACTGTGCGGCATACTTAATTATACATTTGAAACGCGCCCAAGTGACGCT*ag=GGCAAGTCAGAGCAGGTTCCCGTGTTAGCTTAAGGGTAAACATACAAGTC"

    csshort = ":49*ag:50"
    assert shorten(CSTAG) == csshort


def test_deletion():

    csshort = ":39-aagtgacgct:51"

    CSTAG = "=ACTGTGCGGCATACTTAATTATACATTTGAAACGCGCCC-aagtgacgct=AGGCAAGTCAGAGCAGGTTCCCGTGTTAGCTTAAGGGTAAACATACAAGTC"
    assert shorten(CSTAG) == csshort


def test_insertion():

    csshort = ":49+cccccccccc:51"

    CSTAG = "=ACTGTGCGGCATACTTAATTATACATTTGAAACGCGCCCAAGTGACGCT+cccccccccc=AGGCAAGTCAGAGCAGGTTCCCGTGTTAGCTTAAGGGTAAACATACAAGTC"
    assert shorten(CSTAG) == csshort


def test_splicing():

    csshort = ":250~gc1001ag:249"

    CSTAG = "=GTAGGTTGTGAGATGCGGGAGAGGTTCTCGATCTTCCCGTGGGACGTCAACCTTTCCCTTGATAAAGCATCCCGCTCGGGTATGGCAGTGAGTACGCCTTCTGAATTGTGCTATCCTTCGTCCTTATCAAAGCTTGCTACCAATAATTAGGATTATTGCCTTGCGACAGACTTCCTACTCACACTCCCTCACATTGAGCTACTCGATGGGCGATTAGCTTGACCCGCTCTGTAGGGTCGCGACTACGTGA~gc1001ag=CTAAGAGTAGGCCGGGAGTGTAGACCTTTGGGGTTGAATAAATCTATTGTACTAATCGGCTTCAACGAGCCGTACAGGTGGCACCTCAGGAGGGGCCCGCAGGGAGGAAGTAAACTGCTATTCGTCGCCGTTGGTGGTAACTAATTGTGTTCCTTGCCACTACAATTGTATCTAAGCCGTGTAATGAGAACAACCACACCTTAGCGAATTGATGCGCCGCTTCGGAATACCGTTTTGGCTACCCGTTAC"
    assert shorten(CSTAG) == csshort


def test_5bpIns_3bp_Del():

    csshort = ":19+ggggg:20-aag:58"

    CSTAG = (
        "=ACTGTGCGGCATACTTAAT+ggggg=TATACATTTGAAACGCGCCC-aag=TGACGCTAGGCAAGTCAGAGCAGGTTCCCGTGTTAGCTTAAGGGTAAACATACAAGTC"
    )
    assert shorten(CSTAG) == csshort


def test_first_5nt_del_softclip_5nt():

    csshort = ":96"

    CSTAG = "=TGCGGCATACTTAATTATACATTTGAAACGCGCCCAAGTGACGCTAGGCAAGTCAGAGCAGGTTCCCGTGTTAGCTTAAGGGTAAACATACAAGTC"
    assert shorten(CSTAG) == csshort


def test_softclip_plus_5nt():
    csshort = ":100"

    CSTAG = "=ACTGTGCGGCATACTTAATTATACATTTGAAACGCGCCCAAGTGACGCTAGGCAAGTCAGAGCAGGTTCCCGTGTTAGCTTAAGGGTAAACATACAAGTC"
    assert shorten(CSTAG) == csshort


def test_softclip_plusminus_10nt():
    csshort = ":100"

    CSTAG = "=ACTGTGCGGCATACTTAATTATACATTTGAAACGCGCCCAAGTGACGCTAGGCAAGTCAGAGCAGGTTCCCGTGTTAGCTTAAGGGTAAACATACAAGTC"
    assert shorten(CSTAG) == csshort


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

    with open("tests/data/real/tyr_cslong.sam") as f:
        sam_long = [x.strip() for x in f.readlines()]
    contents_long = [s for s in sam_long if not re.search(r"^@", s)]

    cs_shortened = []
    for content in contents_long:
        cs, cigar, seq = call_cs_cigar_seq(content)
        cs_shortened.append(shorten(cs, prefix=True))

    cs_short = []
    for content in contents_short:
        cs, cigar, seq = call_cs_cigar_seq(content)
        cs_short.append(cs)

    for i in range(len(cs_shortened)):
        assert cs_shortened[i] == cs_short[i]
