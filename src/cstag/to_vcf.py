from __future__ import annotations

from itertools import chain
from typing import NamedTuple
from collections import deque, defaultdict, Counter

from cstag.split import split
from cstag.consensus import normalize_read_lengths
from cstag.utils.validator import validate_cs_tag, validate_long_format, validate_pos


class CsInfo(NamedTuple):
    cs_tag: str
    pos_start: int
    pos_end: int
    chrom: str | None = None


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


###########################################################
# Get variant annotations
###########################################################


def find_ref_for_insertion(cs_tag_split: list[str], idx: int) -> str | None:
    idx_ref = idx - 1
    while idx_ref >= 0:
        cs = cs_tag_split[idx_ref]
        if cs[0] in ["=", "-"]:
            return cs[-1].upper()
        if cs.startswith("*"):
            return cs[1].upper()
        idx_ref -= 1
    return None


def find_ref_for_deletion(cs_tag_split: list[str], idx: int) -> str:
    ref = deque([cs_tag_split[idx][1:].upper()])
    idx_ref = idx - 1
    while idx_ref >= 0:
        cs = cs_tag_split[idx_ref]
        if cs.startswith("="):
            ref.appendleft(cs[-1].upper())
            break
        if cs.startswith("*"):
            ref.appendleft(cs[1].upper())
            break
        idx_ref -= 1
    return "".join(ref)


def get_variant_annotations(cs_tag_split: list[str], position: int) -> list[Vcf]:
    variant_annotations = []
    pos = position
    for idx, cs in enumerate(cs_tag_split):
        if cs.startswith("="):
            pos += len(cs) - 1
        elif cs.startswith("*"):
            ref, alt = cs[1].upper(), cs[2].upper()
            variant_annotations.append(Vcf(pos=pos, ref=ref, alt=alt))
            pos += 1
        elif cs.startswith("+"):
            ref = find_ref_for_insertion(cs_tag_split, idx)
            alt = ref + cs[1:].upper()
            variant_annotations.append(Vcf(pos=pos - 1, ref=ref, alt=alt))
        elif cs.startswith("-"):
            ref = find_ref_for_deletion(cs_tag_split, idx)
            variant_annotations.append(Vcf(pos=pos - 1, ref=ref, alt=ref[0]))
        elif cs.startswith("~"):
            continue

    return variant_annotations


###########################################################
# Process CS tag (One)
###########################################################


def process_cs_tag(cs_tag: str, chrom: str, pos: int) -> str:
    validate_cs_tag(cs_tag)
    validate_long_format(cs_tag)
    validate_pos(pos)

    cs_tag_split = split(cs_tag)

    # Call POS, REF, ALT
    variants = get_variant_annotations(cs_tag_split, pos)

    # Write VCF
    HEADER = "##fileformat=VCFv4.2\n#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n"
    vcf = HEADER.strip().split("\n")
    for v in variants:
        vcf.append(f"{chrom}\t{v.pos}\t.\t{v.ref}\t{v.alt}\t.\t.\t.")

    return "\n".join(vcf)


###########################################################
# Format the CS tags
###########################################################


def get_pos_end(cs_tag: str, pos: int) -> int:
    """Get 1-index end positions"""
    pos_end = pos
    for cs in split(cs_tag):
        if cs[0] in ["=", "-"]:
            pos_end += len(cs) - 1
        if cs[0] == "*":
            pos_end += 1
        else:
            continue
    return pos_end


def format_cs_tags(cs_tags: list[str], chroms: list[str] | list[int], positions: list[int]) -> list[CsInfo]:
    """Format and filter cs_tags, and create a list of CsInfo objects.

    This function takes lists of cs_tags, chromosomes, and positions. It filters
    out any cs_tags containing a tilde ("~") and creates a list of CsInfo objects.

    Args:
        cs_tags (list[str]): List of cs_tags as strings.
        chroms (list[str] | list[int]): List of chromosomes as strings or integers.
        positions (list[int]): List of starting positions as integers.

    Returns:
        list[CsInfo]: A list of CsInfo objects, each containing information about
        a cs_tag, its chromosome, and its start and end positions.
    """

    # Convert all chromosomes to string type
    chroms = [str(chrom) for chrom in chroms]
    # Create a list of CsInfo objects, filtering out any with a splicing ("~") in the cs_tag
    cs_info_list = [
        CsInfo(cs_tag=cs, chrom=chrom, pos_start=pos, pos_end=get_pos_end(cs, pos))
        for cs, chrom, pos in zip(cs_tags, chroms, positions)
        if "~" not in cs
    ]
    return cs_info_list


###########################################################
# Group by chrom and overlapping intervals
###########################################################


def group_by_chrom(cs_tags_formatted: list[tuple]) -> dict[str, tuple]:
    """Group CS tags by chromosomes"""
    cs_tags_grouped = defaultdict(list)
    for cs in cs_tags_formatted:
        cs_tags_grouped[cs.chrom].append(
            CsInfo(cs_tag=cs.cs_tag, pos_start=cs.pos_start, pos_end=cs.pos_end, chrom=cs.chrom)
        )
    return dict(cs_tags_grouped)


def group_by_overlapping_intervals(cs_tags_grouped: NamedTuple) -> list[NamedTuple]:
    # Sort the list by the starting point
    sorted_data = sorted(cs_tags_grouped, key=lambda x: x.pos_start)
    # Initialize the list of grouped intervals
    grouped_intervals = []
    # Initialize the first group with the first element
    current_group = [sorted_data[0]]
    # Loop through the sorted list starting from the second element
    for i in range(1, len(sorted_data)):
        overlaps = False
        for j in current_group:
            # Check if the intervals overlap
            if sorted_data[i].pos_start <= j.pos_end and sorted_data[i].pos_end >= j.pos_start:
                overlaps = True
                break
        if overlaps:
            # Add the interval to the current group
            current_group.append(sorted_data[i])
        else:
            # Add the current group to the list of grouped intervals
            grouped_intervals.append(current_group)
            # Start a new group
            current_group = [sorted_data[i]]
    # Add the last group to the list of grouped intervals
    grouped_intervals.append(current_group)

    return grouped_intervals


###########################################################
# Add VCF info
###########################################################


def call_reference_depth(variant_annotations, cs_tags_list, positions_list) -> dict[int, int]:
    positions_min = min(positions_list)
    variant_idx = {v.pos - positions_min for v in variant_annotations}
    variant_pos = {v.pos for v in variant_annotations}
    cs_tags_normalized_length = normalize_read_lengths(cs_tags_list, positions_list)
    # Call ref depth
    reference_depth = defaultdict(int)
    ACGT = {"A", "C", "G", "T"}
    for i, v_pos in zip(variant_idx, variant_pos):
        for cs in cs_tags_normalized_length:
            if cs[i][0] in ACGT:
                reference_depth[v_pos] += 1

    return dict(reference_depth)


def add_vcf_fields(variant_annotations: list[Vcf], chrom: str, reference_depth: dict[int, int]) -> list[Vcf]:
    """Add Chrom and VCF info (AD, RD, DP, and VAF) to VCF NamedTuple"""
    vcf_appended = [v._replace(chrom=chrom) for v in variant_annotations]
    vcf_appended = [v._replace(info=v.info._replace(ad=ad)) for v, ad in Counter(vcf_appended).items()]
    vcf_appended = [v._replace(info=v.info._replace(rd=reference_depth.get(v.pos, 0))) for v in vcf_appended]
    vcf_appended = [v._replace(info=v.info._replace(dp=v.info.rd + v.info.ad)) for v in vcf_appended]
    vcf_appended = [v._replace(info=v.info._replace(vaf=round(v.info.ad / v.info.dp, 3))) for v in vcf_appended]
    return vcf_appended


###########################################################
# Process CS tags (Many)
###########################################################


def chrom_sort_key(chrom: str) -> int:
    """Convert a chromosome string to an integer for sorting."""
    return int(chrom.replace("chr", ""))


def process_cs_tags(cs_tags: list[str], chroms: list[str], positions: list[int]) -> str:
    _ = [validate_cs_tag(cs_tag) for cs_tag in cs_tags]
    _ = [validate_long_format(cs_tag) for cs_tag in cs_tags]
    _ = [validate_pos(pos) for pos in positions]

    cs_tags_formatted = format_cs_tags(cs_tags, chroms, positions)
    cs_tags_grouped_by_chrom = group_by_chrom(cs_tags_formatted)

    vcf_info = []
    for chrom, cs_tags_grouped in cs_tags_grouped_by_chrom.items():
        for csinfo in group_by_overlapping_intervals(cs_tags_grouped):
            cs_tags_list = [cs.cs_tag for cs in csinfo]
            positions_list = [cs.pos_start for cs in csinfo]
            variant_annotations = [
                get_variant_annotations(split(cs), pos) for cs, pos in zip(cs_tags_list, positions_list)
            ]
            variant_annotations = list(chain.from_iterable(variant_annotations))
            if not variant_annotations:
                continue
            reference_depth = call_reference_depth(variant_annotations, cs_tags_list, positions_list)
            vcf_info += add_vcf_fields(variant_annotations, chrom, reference_depth)

    # Sort by chrom and pos
    return sorted(vcf_info, key=lambda x: (chrom_sort_key(x.chrom), x.pos))


###########################################################
# main
###########################################################


def to_vcf(cs_tags: str | list[str], chrom: str | int | list[str] | list[int], pos: int | list[int]) -> str:
    """
    Convert CS tag(s) to VCF (Variant Call Format) string.

    Args:
        cs_tag (str | list[str]): The CS tag representing the sequence alignment.
        chrom (str | list[str]): The chromosome name.
        pos (int | list[int]): The starting position for the sequence.

    Returns:
        str: The VCF-formatted string.
    Example:
        >>> import cstag
        >>> cs_tag = "=AC*gt=T-gg=C+tt=A"
        >>> chrom = "chr1"
        >>> pos = 1
        >>> print(cstag.to_vcf(cstag, chrom, pos))
        ##fileformat=VCFv4.2
        #CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
        chr1	3	.	G	T	.	.	.
        chr1	4	.	TGG	T	.	.	.
        chr1	5	.	C	CTT	.	.	.
    """
    if isinstance(cs_tags, str):
        return process_cs_tag(cs_tags, chrom, pos)
    elif isinstance(cs_tags, list):
        return process_cs_tags(cs_tags, chrom, pos)
    else:
        raise TypeError(f"cs_tags must be str or list, not {type(cs_tags)}")
