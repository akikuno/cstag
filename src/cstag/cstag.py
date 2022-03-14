import re
import sys

def shorten(CSTAG: str, SEQ: str) -> str:
    """Convert long format of cs tag into short format
    Args:
        - CSTAG (str): cs tag in **long** form
        - SEQ (str): segment sequence (10th column in SAM file)
    Returns:
        cs tag in **short** form
    Example:
        >>> import cstag
        >>> seq = "ACGTACGT"
        >>> cstag = "cs:Z:=ACGT*ag=CGT"
        >>> cstag.lengthen(cstag, seq)
        cs:Z::4*ag:3
    """

def lengthen(CSTAG: str, CIGAR: str, SEQ: str) -> str:
    """Convert short format of cs tag into long format
    Args:
        - CSTAG (str): cs tag in **short** form
        - CIGAR (str): CIGAR string (6th column in SAM file)
        - SEQ (str): segment sequence (10th column in SAM file)
    Returns:
        cs tag in **long** form

    Example:
        >>> import cstag
        >>> cstag = "cs:Z::4*ag:3"
        >>> cigar = "8M"
        >>> seq = "ACGTACGT"
        >>> cstag.lengthen(cstag, cigar, seq)
        cs:Z:=ACGT*ag=CGT
    """

    if re.search(r"[ACGT]", CSTAG):
        raise Exception("Error: input cs tag is not short format")

    cstag = re.split(r'([-+*~:])', CSTAG.replace("cs:Z:", ""))[1:]
    cstag = iter(cstag)
    cstag = [i+j for i,j in zip(cstag, cstag)]

    idx = 0
    clips = re.sub(r"^(\d)[SH].*", r"\1", CIGAR)
    if clips.isdigit():
        idx = int(clips)

    cslong = []
    for cs in cstag:
        if cs == "":
            continue
        if cs[0] == ":":
            cs = int(cs[1:]) + idx
            cslong.append(":" + SEQ[idx:cs])
            idx = cs
            continue
        cslong.append(cs)
        if cs[0] == "*":
            idx += 1
        if cs[0] == "+":
            idx += len(cs)-1

    return "cs:Z:" + "".join(cslong).replace(":", "=")
