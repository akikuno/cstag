from __future__ import annotations

import re

from cstag.utils.validator import validate_cs_tag, validate_long_format, validate_threshold


def mask(cs_tag: str, cigar: str, qual: str, threshold: int = 10, prefix: bool = False) -> str:
    """Mask low-quality bases to 'N'
    Args:
        cs_tag (str): cs tag in the **long** format
        cigar (str): cigar strings (6th column in SAM file)
        qual (str): ASCII of Phred-scaled base quaiity+33 (11th column in SAM file)
        threshold (int, optional): Phred Quality Score (defalt = 10). The low-quality bases are defined as 'less than or equal to the threshold'
        prefix (bool, optional): Whether to add the prefix 'cs:Z:' to the cs tag. Defaults to False
    Return:
        str: Masked cs tag
    Example:
        >>> import cstag
        >>> cs_tag = "=ACGT*ac+gg-cc=T"
        >>> cigar = "5M2I2D1M"
        >>> qual = "AA!!!!AA"
        >>> cstag.mask(cs_tag, cigar, qual)
        '=ACNN*an+ng-cc=T'
    """
    validate_cs_tag(cs_tag)
    validate_long_format(cs_tag)
    validate_threshold(threshold)

    mask_symbols = [chr(th + 33) for th in range(threshold + 1)]
    mask_symbols = set(mask_symbols)

    cs = cs_tag.replace("cs:Z:", "")
    list_cs = re.split(r"([-+*~=])", cs)[1:]
    list_cs = [i + j for i, j in zip(list_cs[0::2], list_cs[1::2])]

    if cigar.split("S")[0].isdigit():
        softclip = int(cigar.split("S")[0])
        qual = qual[softclip:]

    cs_masked = []
    idx = 0
    for cs in list_cs:
        cs = list(cs)
        if cs[0] == "*":
            if qual[idx] in mask_symbols:
                cs[-1] = "n"
            idx += 1
        elif cs[0] == "=" or cs[0] == "+":
            for i in range(len(cs) - 1):
                if qual[idx + i] in mask_symbols:
                    cs[i + 1] = "N" if cs[0] == "=" else "n"
            idx += i + 1
        cs_masked.append("".join(cs))
    cs_masked = "".join(cs_masked)

    return f"cs:Z:{cs_masked}" if prefix else cs_masked
