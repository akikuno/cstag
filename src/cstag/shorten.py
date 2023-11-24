from __future__ import annotations

import re


def shorten(cs_tag: str, prefix: bool = False) -> str:
    """Convert long format of cs tag into short format
    Args:
        cs_tag (str): cs tag in the **long** format
        prefix (bool, optional): Whether to add the prefix 'cs:Z:' to the cs tag. Defaults to False
    Return:
        str: cs tag in the **short** format
    Example:
        >>> import cstag
        >>> cs = "=ACGT*ag=CGT"
        >>> cstag.shorten(cs, prefix=True)
        'cs:Z::4*ag:3'
    """
    cstags = re.split(r"([-+*~=])", cs_tag.replace("cs:Z:", ""))[1:]
    cstags = [i + j for i, j in zip(cstags[0::2], cstags[1::2])]

    csshort = []
    for cs in cstags:
        if cs[0] == "=":
            csshort.append(":" + str(len(cs) - 1))
            continue
        csshort.append(cs)
    csshort = "".join(csshort)

    return f"cs:Z:{csshort}" if prefix else csshort
