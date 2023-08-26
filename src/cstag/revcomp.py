from __future__ import annotations

import re
from collections import deque

map_revcomp = {
    "A": "T",
    "C": "G",
    "G": "C",
    "T": "A",
    "N": "N",
    "a": "t",
    "c": "g",
    "g": "c",
    "t": "a",
    "n": "n",
}


def _extract_numbers(strings: str) -> list[str]:
    # Using regular expression to find all numbers in the strings: st
    numbers = re.findall(r"\d+", strings)
    return numbers


def revcomp(cs_tag: str) -> str:
    """Converts a cs tag into its reverse complement.
    Args:
        cs_tag (str): a cs tag
    Return:
        str: reverse complement of a cs tag

    Example:
        >>> import cstag
        >>> cs = "cs:Z::=AAAA*ag=CTG"
        >>> cstag.revcomp(cs)
        cs:Z:=CAG*tc=TTTT
    """
    pattern = r"(\=[ACGTN]+|:[0-9]+|\*[acgtn][acgtn]|\+[acgtn]+|\-[acgtn]+|\~[acgtn]{2}[0-9]+[acgtn]{2})"
    cs_tag_revcomp = deque()
    for cs in re.split(pattern, cs_tag)[::-1]:
        if cs == "":
            continue
        elif cs == "cs:Z:":
            cs_tag_revcomp.appendleft(cs)
        elif cs[0] == ":":
            cs_tag_revcomp.append(cs)
        elif cs[0] == "*":
            cs_tag_revcomp.append(f"*{map_revcomp[cs[1]]}{map_revcomp[cs[2]]}")
        elif cs[0] == "~":
            numbers = _extract_numbers(cs)
            cs_tag_revcomp.append(
                f"~{map_revcomp[cs[-1]]}{map_revcomp[cs[-2]]}{numbers[0]}{map_revcomp[cs[2]]}{map_revcomp[cs[1]]}"
            )
        else:
            op = cs[0]
            cs_revcomp = "".join([map_revcomp[c] for c in cs[1:]])[::-1]
            cs_tag_revcomp.append(f"{op}{cs_revcomp}")
    return "".join(cs_tag_revcomp)
