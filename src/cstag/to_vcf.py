from __future__ import annotations

from cstag.split import split
from collections import deque

from cstag.utils.validator import validate_cs_tag, validate_long_format


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


def get_variant_annotations(cs_tag_split: list[str], position: int) -> list[tuple[int, str, str]]:
    variant_annotations = []
    pos = position
    for idx, cs in enumerate(cs_tag_split):
        if cs.startswith("="):
            pos += len(cs) - 1
        elif cs.startswith("*"):
            ref, alt = cs[1].upper(), cs[2].upper()
            variant_annotations.append((pos, ref, alt))
            pos += 1
        elif cs.startswith("+"):
            ref = find_ref_for_insertion(cs_tag_split, idx)
            alt = ref + cs[1:].upper()
            variant_annotations.append((pos - 1, ref, alt))
        elif cs.startswith("-"):
            ref = find_ref_for_deletion(cs_tag_split, idx)
            variant_annotations.append((pos - 1, ref, ref[0]))
        elif cs.startswith("~"):
            continue

    return variant_annotations


###########################################################
# main
###########################################################


def to_vcf(cs_tag: str, chrom: str, pos: int) -> str:
    """
    Convert a CS tag to VCF (Variant Call Format) string.

    Args:
        cs_tag (str): The CS tag representing the sequence alignment.
        chrom (str): The chromosome name.
        pos (int): The starting position for the sequence.

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
    validate_cs_tag(cs_tag)
    validate_long_format(cs_tag)

    cs_tag_split = split(cs_tag)

    # Call POS, REF, ALT
    variants = get_variant_annotations(cs_tag_split, pos)

    # Write VCF
    HEADER = "##fileformat=VCFv4.2\n#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO\n"

    vcf = HEADER.strip().split("\n")
    for pos, ref, alt in variants:
        vcf.append(f"{chrom}\t{pos}\t.\t{ref}\t{alt}\t.\t.\t.")

    return "\n".join(vcf)
