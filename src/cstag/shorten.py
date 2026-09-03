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
    cstags = [
        operation + value
        for operation, value in zip(cstags[0::2], cstags[1::2], strict=False)
    ]

    short_operations: list[str] = []
    for cs in cstags:
        if cs[0] == "=":
            short_operations.append(":" + str(len(cs) - 1))
            continue
        short_operations.append(cs)
    cs_short = "".join(short_operations)

    return f"cs:Z:{cs_short}" if prefix else cs_short
