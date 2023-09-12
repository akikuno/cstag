from typing import NamedTuple
from src.cstag.to_vcf import find_ref_for_insertion, find_ref_for_deletion, get_variant_annotations, process_cs_tag


class VcfInfo(NamedTuple):
    dp: int | None = None
    rd: int | None = None
    ad: int | None = None
    vaf: float | None = None


class Vcf(NamedTuple):
    chrom: str | None = None
    pos: int | None = None
    ref: str | None = None
    alt: str | None = None
    info: VcfInfo = VcfInfo()


# find_ref_for_insertionのテスト
def test_find_ref_for_insertion():
    assert find_ref_for_insertion(["=ACGT", "*ga", "+a"], 0) is None
    assert find_ref_for_insertion(["=ACGT", "*ga", "+a"], 1) == "T"
    assert find_ref_for_insertion(["=ACGT", "*ga", "+a"], 2) == "G"
    assert find_ref_for_insertion(["=AC", "=GT", "-g", "+a"], 3) == "G"


# find_ref_for_deletionのテスト
def test_find_ref_for_deletion():
    assert find_ref_for_deletion(["=AC", "-g"], 1) == "CG"
    assert find_ref_for_deletion(["=ACGT", "*ga", "-a"], 2) == "GA"
    assert find_ref_for_deletion(["=ACGT", "*ga", "-ac"], 2) == "GAC"
    assert find_ref_for_deletion(["=AC", "=GT", "+a", "-a"], 3) == "TA"


# get_variant_annotationsのテスト
def test_get_variant_annotations():
    default_info = VcfInfo()
    # single mutation
    assert get_variant_annotations(["=AC", "*ga", "=AC"], 1) == [Vcf(None, 3, "G", "A", info=default_info)]
    assert get_variant_annotations(["=AC", "+a", "=AC"], 1) == [Vcf(None, 2, "C", "CA", info=default_info)]
    assert get_variant_annotations(["=AC", "-a", "=AC"], 1) == [Vcf(None, 2, "CA", "C", info=default_info)]

    # double mutations
    assert get_variant_annotations(["=AC", "*ga", "=AC", "*ct"], 1) == [
        Vcf(None, 3, "G", "A", info=default_info),
        Vcf(None, 6, "C", "T", info=default_info),
    ]
    assert get_variant_annotations(["=AC", "+a", "=AC", "+aa"], 1) == [
        Vcf(None, 2, "C", "CA", info=default_info),
        Vcf(None, 4, "C", "CAA", info=default_info),
    ]
    assert get_variant_annotations(["=AC", "-a", "=AC", "-aa"], 1) == [
        Vcf(None, 2, "CA", "C", info=default_info),
        Vcf(None, 4, "CAA", "C", info=default_info),
    ]

    # combinations
    assert get_variant_annotations(["=ACGT", "*ga", "+a"], 1) == [
        Vcf(None, 5, "G", "A", info=default_info),
        Vcf(None, 5, "G", "GA", info=default_info),
    ]
    assert get_variant_annotations(["=ACGT", "*ga", "-a"], 1) == [
        Vcf(None, 5, "G", "A", info=default_info),
        Vcf(None, 5, "GA", "G", info=default_info),
    ]
    assert get_variant_annotations(["=ACGT", "*ga", "-ac"], 1) == [
        Vcf(None, 5, "G", "A", info=default_info),
        Vcf(None, 5, "GAC", "G", info=default_info),
    ]
    # position
    assert get_variant_annotations(["=AC", "*ga", "=AC", "*ct"], 10) == [
        Vcf(None, 12, "G", "A", info=default_info),
        Vcf(None, 15, "C", "T", info=default_info),
    ]


# process_cs_tag関数のテスト
def test_process_cs_tag():
    cs_tag1 = "=AC*gt=T-gg=C+tt=A"
    chrom1 = "chr1"
    pos1 = 1
    expected_output1 = """##fileformat=VCFv4.2
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
chr1	3	.	G	T	.	.	.
chr1	4	.	TGG	T	.	.	.
chr1	5	.	C	CTT	.	.	."""
    assert process_cs_tag(cs_tag1, chrom1, pos1) == expected_output1

    cs_tag2 = "=AC*ga"
    chrom2 = "2"
    pos2 = 1
    expected_output2 = """##fileformat=VCFv4.2
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
2	3	.	G	A	.	.	."""
    assert process_cs_tag(cs_tag2, chrom2, pos2) == expected_output2
