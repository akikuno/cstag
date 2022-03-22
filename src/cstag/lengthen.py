import re

def lengthen(CSTAG: str, CIGAR: str, SEQ: str) -> str:
    """Convert short format of cs tag into long format
    Args:
        CSTAG (str): cs tag in **short** form
        CIGAR (str): CIGAR string (6th column in SAM file)
        SEQ (str): segment sequence (10th column in SAM file)
    Return:
        str: cs tag in **long** form

    Example:
        >>> import cstag
        >>> cs = "cs:Z::4*ag:3"
        >>> cigar = "8M"
        >>> seq = "ACGTACGT"
        >>> cstag.lengthen(cs, cigar, seq)
        cs:Z:=ACGT*ag=CGT
    """

    if re.search(r"[ACGT]", CSTAG):
        raise Exception("Error: input cs tag is not short format")

    cstags = re.split(r"([-+*~:])", CSTAG.replace("cs:Z:", ""))[1:]
    cstags = [i + j for i, j in zip(cstags[0::2], cstags[1::2])]

    softclip = re.sub(r"^([0-9]+)S.*", r"\1", CIGAR)
    idx = int(softclip) if softclip.isdigit() else 0

    cslong = []
    for cs in cstags:
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
            idx += len(cs) - 1

    return "cs:Z:" + "".join(cslong).replace(":", "=")
