from __future__ import annotations

from src.cstag.to_vcf import (
    Vcf,
    VcfInfo,
    chrom_sort_key,
    find_ref_for_insertion,
    find_ref_for_deletion,
    get_variant_annotations,
    get_pos_end,
    add_vcf_fields,
    process_cs_tag,
    process_cs_tags,
)

###########################################################
# Get variant annotations
###########################################################


def test_find_ref_for_insertion():
    assert find_ref_for_insertion(["=ACGT", "*ga", "+a"], 0) is None
    assert find_ref_for_insertion(["=ACGT", "*ga", "+a"], 1) == "T"
    assert find_ref_for_insertion(["=ACGT", "*ga", "+a"], 2) == "G"
    assert find_ref_for_insertion(["=AC", "=GT", "-g", "+a"], 3) == "G"


def test_find_ref_for_deletion():
    assert find_ref_for_deletion(["=AC", "-g"], 1) == "CG"
    assert find_ref_for_deletion(["=ACGT", "*ga", "-a"], 2) == "GA"
    assert find_ref_for_deletion(["=ACGT", "*ga", "-ac"], 2) == "GAC"
    assert find_ref_for_deletion(["=AC", "=GT", "+a", "-a"], 3) == "TA"


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


###########################################################
# Format the CS tags
###########################################################


def test_get_pos_end():
    assert get_pos_end("=ACGT", 1) == 4
    assert get_pos_end("=ACGT", 5) == 8
    assert get_pos_end("=ACGT*ag=ACGT", 1) == 9
    assert get_pos_end("=ACGT-aa=ACGT", 1) == 10
    assert get_pos_end("=ACGT+aa=ACGT", 1) == 8
    assert get_pos_end("=ACGTNNACGT", 1) == 10


###########################################################
# Group by chrom and overlapping intervals
###########################################################


###########################################################
# Add VCF info
###########################################################


def test_add_vcf_fields():
    sample_variant_annotations = [
        Vcf(chrom=None, pos=1, ref="A", alt="T", info=VcfInfo(dp=None, rd=None, ad=None, vaf=None)),
        Vcf(chrom=None, pos=1, ref="A", alt="T", info=VcfInfo(dp=None, rd=None, ad=None, vaf=None)),
        Vcf(chrom=None, pos=2, ref="G", alt="C", info=VcfInfo(dp=None, rd=None, ad=None, vaf=None)),
    ]
    sample_chrom = "chr1"
    sample_reference_depth = {1: 10, 2: 5}
    result = add_vcf_fields(sample_variant_annotations, sample_chrom, sample_reference_depth)
    result = sorted(result, key=lambda x: (chrom_sort_key(x.chrom), x.pos))
    assert result[0].chrom == "chr1"
    assert result[0].info.ad == 2
    assert result[0].info.rd == 10
    assert result[0].info.dp == 12
    assert result[0].info.vaf == 0.167
    assert result[1].chrom == "chr1"
    assert result[1].info.ad == 1
    assert result[1].info.rd == 5
    assert result[1].info.dp == 6
    assert result[1].info.vaf == 0.167


###########################################################
# process_cs_tag: Single CS tag
###########################################################


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


###########################################################
# process_cs_tags: Multuple CS tags
###########################################################


def test_process_cs_tags_base():
    cs_tags = ["=ACGT", "=AC*gt=T", "=C*gt=T", "=ACGT", "=AC*gt=T", "=AC~nn10nn=GT"]
    chroms = ["chr1", "chr1", "chr1", "chr2", "chr2", "chr3"]
    positions = [2, 2, 3, 10, 100, 5]
    expected_output = """##fileformat=VCFv4.2\n##INFO=<ID=DP,Number=1,Type=Integer,Description="Total Depth">\n##INFO=<ID=RD,Number=1,Type=Integer,Description="Depth of Ref allele">\n##INFO=<ID=AD,Number=1,Type=Integer,Description="Depth of Alt allele">\n##INFO=<ID=VAF,Number=1,Type=Float,Description="Variant allele fractions (AD/DP)">\n#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\nchr1\t4\t.\tG\tT\t.\t.\tDP=3;RD=1;AD=2;VAF=0.667\nchr2\t102\t.\tG\tT\t.\t.\tDP=1;RD=0;AD=1;VAF=1.0"""
    assert process_cs_tags(cs_tags, chroms, positions) == expected_output


# def test_process_cs_tags_crhoms_sort():
#     cs_tags = ["=ACGT", "=AC*gt=T", "=C*gt=T", "=ACGT", "=AC*gt=T", "=AC*gt=T"]
#     chroms = ["chr1", "chr1", "chr1", "chr2", "chr10", "chr2"]
#     positions = [2, 2, 3, 10, 100, 5]
#     expected_output = """##fileformat=VCFv4.2\n##INFO=<ID=DP,Number=1,Type=Integer,Description="Total Depth">\n##INFO=<ID=RD,Number=1,Type=Integer,Description="Depth of Ref allele">\n##INFO=<ID=AD,Number=1,Type=Integer,Description="Depth of Alt allele">\n##INFO=<ID=VAF,Number=1,Type=Float,Description="Variant allele fractions (AD/DP)">\n#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\nchr1\t4\t.\tG\tT\t.\t.\tDP=3;RD=1;AD=2;VAF=0.667\nchr2\t102\t.\tG\tT\t.\t.\tDP=1;RD=0;AD=1;VAF=1.0"""
#     assert process_cs_tags(cs_tags, chroms, positions) == expected_output
