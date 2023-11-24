from __future__ import annotations

import re


def split(cs_tag: str, prefix: bool = False) -> list[str]:
    """Split a cs tag
    Args:
        cs_tag (str): a cs tag
        prefix (bool, optional): Whether to add the prefix 'cs:Z:' to the cs tag. Defaults to False
    Return:
        list[str]: splits a cs tag by operators

    Example:
        >>> import cstag
        >>> cs = ":4*ag:3"
        >>> cstag.split(cs)
        [':4', '*ag', ':3']
    """
    cs_tag = cs_tag.replace("cs:Z:", "")

    pattern = r"(\=[ACGTN]+|:[0-9]+|\*[acgtn][acgtn]|\+[acgtn]+|\-[acgtn]+|\~[acgtn]{2}[0-9]+[acgtn]{2})"
    cs_split = [cs for cs in re.split(pattern, cs_tag) if cs]

    if prefix is True:
        return ["cs:Z:"] + cs_split
    else:
        return cs_split
