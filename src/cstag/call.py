from __future__ import annotations

import re
from cstag.shorten import shorten

###########################################################
# Define the mapping between the mutation and key
###########################################################

# use arbitrary characters other than 'acgtn' for keys, which are used for deletions.
mutation_to_key = {
    "*ac": "b",
    "*ag": "d",
    "*at": "h",
    "*ca": "v",
    "*cg": "x",
    "*ct": "y",
    "*ga": "m",
    "*gc": "r",
    "*gt": "k",
    "*ta": "w",
    "*tc": "s",
    "*tg": "o",
}
key_to_mutation = {v: k for k, v in mutation_to_key.items()}


###########################################################
# Trim soft and hard clips from the CIGAR and sequence
###########################################################


def _split_cigar(cigar: str) -> list[tuple(str, int)]:
    parsed_cigar = []
    start_idx = 0
    for idx, operation in enumerate(cigar):
        if operation.isdigit():
            continue
        length = int(cigar[start_idx:idx])
        parsed_cigar.append((operation, length))
        start_idx = idx + 1
    return parsed_cigar


def _join_cigar(cigar_tuples: list[tuple[str, int]]) -> str:
    return "".join(f"{length}{operation}" for operation, length in cigar_tuples)


def trim_clips(cigar: str, seq: str) -> tuple(str, str):
    if all(x not in cigar for x in "SH"):
        return cigar, seq
    cigar_split = _split_cigar(cigar)
    # trim soft clips of cigar and seq
    if cigar_split[0][0] == "S":
        length_softclip = cigar_split[0][1]
        seq = seq[length_softclip:]
        cigar_split = cigar_split[1:]
    if cigar_split[-1][0] == "S":
        length_softclip = cigar_split[-1][1]
        seq = seq[:-length_softclip]
        cigar_split = cigar_split[:-1]
    # trim hard clips of cigar
    if cigar_split[0][0] == "H":
        cigar_split = cigar_split[1:]
    if cigar_split[-1][0] == "H":
        cigar_split = cigar_split[:-1]
    cigar = _join_cigar(cigar_split)
    return cigar, seq


def _split_md(md: str) -> list[tuple(str, int)]:
    parsed_md = []
    idx = 0
    while idx < len(md):
        if md[idx].isdigit():
            start = idx
            while idx < len(md) and md[idx].isdigit():
                idx += 1
            parsed_md.append(("=", int(md[start:idx])))
        elif md[idx] == "^":  # Deletion
            start = idx
            idx += 1
            while idx < len(md) and not md[idx].isdigit():
                idx += 1
            parsed_md.append((md[start:idx], idx - start - 1))
        else:  # Mismatch
            parsed_md.append((md[idx], 1))
            idx += 1
    return parsed_md


def generate_cslong_md_based(seq: str, md: str) -> list[str]:
    md_split = _split_md(md)
    cslong_md_based = []
    idx = 0
    for op, length in md_split:
        if op == "=":
            cslong_md_based.append(f"={seq[idx:idx+length]}")
            idx += length
        elif op.startswith("^"):
            cslong_md_based.append(f"-{op[1:].lower()}")
        else:
            cslong_md_based.append(f"*{op}{seq[idx]}".lower())
            idx += 1
    return cslong_md_based


def align_length(cslong_md_based: list[str]) -> str:
    str_cslong = []
    for cs in cslong_md_based:
        if cs.startswith("*"):
            str_cslong.append(mutation_to_key[cs])
        else:
            str_cslong.append(cs[1:])
    return "".join(str_cslong)


def generate_cslong_cigar_integrated(cigar: str, str_cslong: str) -> str:
    cigar_split = _split_cigar(cigar)
    idx_n = 0
    cslong = []
    for op, length in cigar_split:
        if op == "N":
            cslong.append(f"~nn{length}nn")
        elif op == "I":
            cslong.append(f"+{str_cslong[idx_n:idx_n+length]}".lower())
            idx_n += length
        elif op == "D":
            cslong.append(f"-{str_cslong[idx_n:idx_n+length]}".lower())
            idx_n += length
        else:
            cslong.append(f"={str_cslong[idx_n:idx_n+length]}")
            idx_n += length
    return "".join(cslong)


def revert_substitution(cslong: str) -> str:
    cslong_split = re.split(r"([bdhvxymrkwso])", cslong)
    for i, cs in enumerate(cslong_split):
        if cs in key_to_mutation:
            cslong_split[i] = key_to_mutation[cs]
        elif cs[0] not in {"=", "-", "+", "*", "~"}:
            cslong_split[i] = f"={cs}"
    return "".join(cslong_split)


def add_prefix(cslong: str) -> str:
    return f"cs:Z:{cslong}"


###########################################################
# main
###########################################################


def call(cigar: str, md: str, seq: str, is_short_form: bool = True) -> str:
    cigar, seq = trim_clips(cigar, seq)
    cslong_md_based = generate_cslong_md_based(seq, md)
    str_cslong = align_length(cslong_md_based)
    cslong = generate_cslong_cigar_integrated(cigar, str_cslong)
    cslong_update = revert_substitution(cslong)
    cslong_update = add_prefix(cslong_update)
    if is_short_form:
        cslong_update = shorten(cslong_update)
    return cslong_update
