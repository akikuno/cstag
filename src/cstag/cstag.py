import re
import sys

def shorten(sam: list) -> list:
    """Convert long format of cs tag into short format

    Args:
        sam (list): List of SAM (Sequence Alignment/Map Format) including a cs tag in **long** form

    Returns:
        List of SAM including a cs tag in **short** form

    Example:
        >>> import cstag
        >>> sam = [hoge]
        >>> cstag.shorten(sam)
        [hoge]
    """
    print("Hello!!")

def lengthen(CSTAG: chr, SEQ: chr) -> chr:
    """Convert short format of cs tag into long format
    Args:
        sam (list): List of SAM (Sequence Alignment/Map Format) including a cs tag in **short** form

    Returns:
        List of SAM including a cs tag in **long** form

    Example:
        >>> import cstag
        >>> sam = [hoge]
        >>> cstag.lengthen(sam)
        [hoge]
    """
    cstag = re.split('([-+*~:])', CSTAG.replace("cs:Z:", ""))[1:]
    cstag = iter(cstag)
    cstag = [i+j for i,j in zip(cstag, cstag)]

    idx = 0
    cslong = []
    for cs in cstag:
        if cs == "":
            continue
        if cs[0] == ":":
            cs = int(cs[1:]) + idx
            cslong.append(":" + SEQ[idx:cs])
            idx += cs
            continue
        cslong.append(cs)
        if cs[0] == "*":
            idx += 1
        if cs[0] == "+":
            idx += len(cs)-1

    return "cs:Z:" + "".join(cslong).replace(":", "=")