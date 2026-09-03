from __future__ import annotations

import re

from .utils.validator import validate_cs_tag, validate_short_format


def lengthen(cs_tag: str, cigar: str, seq: str, prefix: bool = False) -> str:
    """Convert short format of cs tag into long format
    Args:
        cs_tag (str): cs tag in **short** form
        cigar (str): CIGAR string (6th column in SAM file)
        seq (str): segment sequence (10th column in SAM file)
        prefix (bool, optional): Whether to add the prefix 'cs:Z:' to the cs tag. Defaults to False

    Return:
        str: cs tag in **long** form

    Example:
        >>> import cstag
        >>> cs = ":4*ag:3"
        >>> cigar = "8M"
        >>> seq = "ACGTACGT"
        >>> cstag.lengthen(cs, cigar, seq)
        '=ACGT*ag=CGT'
    """
    validate_cs_tag(cs_tag)
    validate_short_format(cs_tag)

    cs_tag_split = re.split(r"([-+*~:])", cs_tag.replace("cs:Z:", ""))[1:]
    cs_tag_split = [
        operation + value
        for operation, value in zip(cs_tag_split[0::2], cs_tag_split[1::2], strict=True)
    ]

    softclip = re.sub(r"^([0-9]+)S.*", r"\1", cigar)
    idx = int(softclip) if softclip.isdigit() else 0

    long_operations: list[str] = []
    for cs in cs_tag_split:
        if cs == "":
            continue
        if cs[0] == ":":
            match_end = int(cs[1:]) + idx
            long_operations.append(":" + seq[idx:match_end])
            idx = match_end
            continue
        long_operations.append(cs)
        if cs[0] == "*":
            idx += 1
        if cs[0] == "+":
            idx += len(cs) - 1
    cs_long = "".join(long_operations).replace(":", "=")

    return f"cs:Z:{cs_long}" if prefix else cs_long
