import re
from itertools import chain
from collections import deque, Counter

def consensus(CSTAG: list, CIGAR: list, POS: list) -> str:
    """
    ###
    """
    if not (len(CSTAG) == len(CIGAR) == len(POS)):
        raise Exception("Error: Element numbers of each argument must be the same")

    pos_min = min(POS)
    pos = [pos - pos_min for pos in POS]

    softclips = [re.sub(r"^([0-9]+)S.*", r"\1", cigar) for cigar in CIGAR]
    softclips = [int(s) if s.isdigit() else 0 for s in softclips]

    starts = [p+s for p, s in zip(pos, softclips)]

    cs_list = []
    for cs in CSTAG:
        cs = cs.replace("cs:Z:", "")
        cs = re.split(r'([-*~=])', cs)[1:]
        cs = [i+j for i,j in zip(cs[0::2], cs[1::2])]
        cs = [c.replace("=", "") for c in cs]
        cs = [re.split(r"(?=[ACGT])", c) for c in cs]
        cs = [list(filter(None, c)) for c in cs]
        cs = list(chain.from_iterable(cs))
        cs_list.append(deque(cs))

    cs_maxlen = max(len(c) for c in cs_list)
    for i, (cs, start) in enumerate(zip(cs_list, starts)):
        if start:
            cs_list[i].appendleft("N" * start)
        if len(cs_list[i]) < cs_maxlen:
            cs_list[i].append("N" * cs_maxlen - len(cs_list[i]))

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

    return "cs:Z:" + re.sub(r"([ACGT]+)", r"=\1", cs_consensus)
