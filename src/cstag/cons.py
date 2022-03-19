import re
from itertools import chain
from collections import deque, Counter


def consensus(CSTAG: list, CIGAR: list, POS: list) -> str:
    """generate consensus of cs tags
    Args:
        CSTAG (list): cs tags in the **long** format
        CIGAR (list): CIGAR strings (6th column in SAM file)
        POS (list): 1-based leftmost mapping position (4th column in SAM file)
    Return:
        str: a consensus of cs tag in the **long** format
    Example:
        >>> import cstag
        >>> cs_list = ["cs:Z:=ACGT", "cs:Z:=AC*gt=T", "cs:Z:=C*gt=T", "cs:Z:=C*gt=T", "cs:Z:=ACT+ccc=T"]
        >>> cigar_list = ["4M","4M","1S3M", "3M", "3M3I1M"]
        >>> pos_list = [6,6,6,7,6]
        >>> cstag.consensus(cs_list, cigar_list, pos)
        cs:Z:=AC*gt*T
    """
    if not (len(CSTAG) == len(CIGAR) == len(POS)):
        raise Exception("Error: Element numbers of each argument must be the same")

    if not all(re.search(r"[ACGT]", cs) for cs in CSTAG):
        raise Exception("Error: cs tag must be a long format")

    pos_min = min(POS)
    pos = [pos - pos_min for pos in POS]

    softclips = [re.sub(r"^([0-9]+)S.*", r"\1", cigar) for cigar in CIGAR]
    softclips = [int(s) if s.isdigit() else 0 for s in softclips]

    starts = [p + s for p, s in zip(pos, softclips)]

    cs_list = []
    for cs in CSTAG:
        cs = cs.replace("cs:Z:", "")
        cs = re.split(r"([-*~=])", cs)[1:]
        cs = [i + j for i, j in zip(cs[0::2], cs[1::2])]
        cs = [c.replace("=", "") for c in cs]
        cs = [re.split(r"(?=[ACGT])", c) for c in cs]
        cs = [list(filter(None, c)) for c in cs]
        cs = list(chain.from_iterable(cs))
        cs_list.append(deque(cs))

    cs_maxlen = max(len(cs) + start for cs, start in zip(cs_list, starts))
    for i, (cs, start) in enumerate(zip(cs_list, starts)):
        if start:
            cs_list[i].extendleft(["N"] * start)
        if len(cs_list[i]) < cs_maxlen:
            cs_list[i].extend(["N"] * (cs_maxlen - len(cs_list[i])))

    def get_consensus(cs: tuple) -> str:
        """
        When it is multimodal, return the first **mutated** mode encountered
        """
        mostcommon = Counter(cs).most_common(1)
        if len(mostcommon) == 1:
            return mostcommon[0][0]
        for key, val in mostcommon:
            if not re.search(r"[ACGT]", key):
                return key

    cs_consensus = [get_consensus(cs) for cs in list(zip(*cs_list))]
    cs_consensus = "".join(cs_consensus)

    return "cs:Z:" + re.sub(r"([ACGTN]+)", r"=\1", cs_consensus)
