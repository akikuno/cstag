import re

def lengthen(cs_tag: str, cigar: str, seq: str) -> str:
    """Convert short format of cs tag into long format
    Args:
        cs_tag (str): cs tag in **short** form
        cigar (str): CIGAR string (6th column in SAM file)
        seq (str): segment sequence (10th column in SAM file)
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

    if re.search(r"[ACGT]", cs_tag):
        raise Exception("Error: input cs tag is not short format")

    cs_tag_split = re.split(r"([-+*~:])", cs_tag.replace("cs:Z:", ""))[1:]
    cs_tag_split = [i + j for i, j in zip(cs_tag_split[0::2], cs_tag_split[1::2])]

    softclip = re.sub(r"^([0-9]+)S.*", r"\1", cigar)
    idx = int(softclip) if softclip.isdigit() else 0

    cslong = []
    for cs in cs_tag_split:
        if cs == "":
            continue
        if cs[0] == ":":
            cs = int(cs[1:]) + idx
            cslong.append(":" + seq[idx:cs])
            idx = cs
            continue
        cslong.append(cs)
        if cs[0] == "*":
            idx += 1
        if cs[0] == "+":
            idx += len(cs) - 1

    return "cs:Z:" + "".join(cslong).replace(":", "=")
