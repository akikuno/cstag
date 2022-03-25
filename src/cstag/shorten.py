import re


def shorten(CSTAG: str) -> str:
    """Convert long format of cs tag into short format
    Args:
        CSTAG (str): cs tag in the **long** format
    Return:
        str: cs tag in the **short** format
    Example:
        >>> import cstag
        >>> cs = "cs:Z:=ACGT*ag=CGT"
        >>> cstag.shorten(cs)
        cs:Z::4*ag:3
    """
    cstags = re.split(r"([-+*~=])", CSTAG.replace("cs:Z:", ""))[1:]
    cstags = [i + j for i, j in zip(cstags[0::2], cstags[1::2])]

    csshort = []
    for cs in cstags:
        if cs[0] == "=":
            csshort.append(":" + str(len(cs) - 1))
            continue
        csshort.append(cs)

    return "cs:Z:" + "".join(csshort)

