from __future__ import annotations

import re


def split(cs_tag: str) -> list[str]:
    """Split a cs tag
    Args:
        cs_tag (str): a cs tag
    Return:
        list[str]: splits a cs tag by operators

    Example:
        >>> import cstag
        >>> cs = "cs:Z::4*ag:3"
        >>> cstag.split(cs)
        ["cs:Z:", ":4", "*ag", ":3"]
    """
    pattern = r"(\=[ACGTN]+|:[0-9]+|\*[acgtn][acgtn]|\+[acgtn]+|\-[acgtn]+|\~[acgtn]{2}[0-9]+[acgtn]{2})"
    return [cs for cs in re.split(pattern, cs_tag) if cs]
