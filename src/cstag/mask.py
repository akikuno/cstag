import re


def mask(CSTAG: str, CIGAR: str, QUAL: str, THRESHOLD: int = 10):
    """Mask low-quality bases to 'N'
    Args:
        CSTAG (str): cs tag in the **long** format
        CIGAR (str): CIGAR strings (6th column in SAM file)
        QUAL (str): ASCII of Phred-scaled base quaiity+33 (11th column in SAM file)
        THRESHOLD (int): optional: Phred Quality Score (defalt = 10). The low-quality bases are defined as 'less than or equal to the threshold'
    Return:
        str: Masked cs tag
    Example:
        >>> import cstag
        >>> CSTAG = "cs:Z:=ACGT*ac+gg-cc=T"
        >>> CIGAR = "5M2I2D1M"
        >>> QUAL = "AA!!!!AA"
        >>> cstag.mask(CSTAG, QUAL)
        cs:Z:=ACNN*an+ng-cc=T
    """
    if not re.search(r"[ACGT]", CSTAG):
        raise Exception("Error: cs tag must be a long format")
    if not isinstance(THRESHOLD, int):
        raise Exception("Error: threshold must be an integer")
    if not 0 <= THRESHOLD <= 40:
        raise Exception("Error: threshold must be within a range between 0 to 40")

    mask_symbols = [chr(th + 33) for th in range(THRESHOLD + 1)]
    mask_symbols = set(mask_symbols)

    cs = CSTAG.replace("cs:Z:", "")
    list_cs = re.split(r"([-+*~=])", cs)[1:]
    list_cs = [i + j for i, j in zip(list_cs[0::2], list_cs[1::2])]

    if CIGAR.split("S")[0].isdigit():
        softclip = int(CIGAR.split("S")[0])
        QUAL = QUAL[softclip:]

    cs_masked = []
    idx = 0
    for cs in list_cs:
        cs = list(cs)
        if cs[0] == "*":
            if QUAL[idx] in mask_symbols:
                cs[-1] = "n"
            idx += 1
        elif cs[0] == "=" or cs[0] == "+":
            for i in range(len(cs) - 1):
                if QUAL[idx + i] in mask_symbols:
                    cs[i + 1] = "N" if cs[0] == "=" else "n"
            idx += i + 1
        cs_masked.append("".join(cs))

    return "cs:Z:" + "".join(cs_masked)
