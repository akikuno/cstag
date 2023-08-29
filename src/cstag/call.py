from __future__ import annotations

import re
from cstag.shorten import shorten

###########################################################
# Define the mapping between the mutation and key
###########################################################

# use arbitrary characters other than 'acgtn' for keys, which are used for deletions.
mutation_encoding = {
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
mutation_decoding = {v: k for k, v in mutation_encoding.items()}


###########################################################
# Trim soft and hard clips from the CIGAR and sequence
###########################################################


def _split_cigar(cigar: str) -> list[tuple[str, int]]:
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


def trim_clips(cigar: str, seq: str) -> tuple[str, str]:
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


def _split_md(md: str) -> list[tuple[str, int]]:
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


def generate_cslong_md(seq: str, md: str) -> list[str]:
    md_split = _split_md(md)
    cslong_md = []
    idx = 0
    for op, length in md_split:
        if op == "=":
            cslong_md.append(f"={seq[idx:idx+length]}")
            idx += length
        elif op.startswith("^"):
            cslong_md.append(f"-{op[1:].lower()}")
        else:
            cslong_md.append(f"*{op}{seq[idx]}".lower())
            idx += 1
    """trim only operators:
    if md contains zero, it contains only op.
    eg. md = "0C3T0" -> ['=', '*ca', '=AAA', '*tc', '=']
    these '='s should be trimmed.
    """
    cslong_md = [c for c in cslong_md if len(c) > 1]
    return cslong_md


def _encode_substitution(cslong_with_substitutions: list[str]) -> str:
    """
    Convert substitution representations like '*ac', '*ag', etc., to single characters.

    The function aims to make the length of the sequence uniform for easier handling.
    For example, if the original sequence 'ACGT' has 'G' substituted by 'A',
    it would be represented as 'AC*agT'. To make the sequence length uniform,
    this function would convert it to 'ACdT'.
    """
    cslong_converted = []
    for cs_element in cslong_with_substitutions:
        if cs_element.startswith("*"):
            cslong_converted.append(mutation_encoding[cs_element])
        else:
            cslong_converted.append(cs_element[1:])
    return "".join(cslong_converted)


def remove_equal_sign(text: str) -> str:
    # Retain occurrences of "=[ACGTN]" and remove all other "=" signs
    return re.sub(r"=(?![ACGT])", "", text)


def generate_cslong_cigar_integrated(cigar: str, cslong_md: list[str]) -> list[str]:
    cigar_split = _split_cigar(cigar)
    cslong_encoded = _encode_substitution(cslong_md)
    idx_n = 0
    cslong_md_cigar = []
    for op, length in cigar_split:
        if op == "N":
            cslong_md_cigar.append(f"~nn{length}nn")
        elif op == "I":
            cslong_md_cigar.append(f"+{cslong_encoded[idx_n:idx_n+length]}".lower())
            idx_n += length
        elif op == "D":
            cslong_md_cigar.append(f"-{cslong_encoded[idx_n:idx_n+length]}".lower())
            idx_n += length
        else:
            cslong_md_cigar.append(f"={cslong_encoded[idx_n:idx_n+length]}")
            idx_n += length
    return [remove_equal_sign(cs) for cs in cslong_md_cigar]


def decode_substitution(cslong_md_cigar: list[str]) -> list[str]:
    cslong_decoded = [c for c in re.split(r"([bdhvxymrkwso])", "".join(cslong_md_cigar)) if c]
    for i, cs in enumerate(cslong_decoded):
        if cs in mutation_decoding:
            cslong_decoded[i] = mutation_decoding[cs]
        elif cs[0] not in {"=", "-", "+", "*", "~"}:
            cslong_decoded[i] = f"={cs}"
    return cslong_decoded


def add_prefix(cs_tag: str) -> str:
    return f"cs:Z:{cs_tag}"


###########################################################
# main
###########################################################


def call(cigar: str, md: str, seq: str, is_long: bool = False, prefix: bool = False) -> str:
    """
    Generate a cs tag based on CIGAR, MD, and SEQ information.

    Args:
        cigar (str): CIGAR string representing the alignment.
        md (str): MD tag representing mismatching positions/base.
        seq (str): The sequence of the read.
        is_long (bool, optional): Whether to return the cs tag in long format. Defaults to False.
        prefix (bool, optional): Whether to add the prefix 'cs:Z:' to the cs tag. Defaults to False

    Returns:
        str: A cs tag representing the alignment and differences.

    Example:
        >>> import your_module  # Replace 'your_module' with the actual module name
        >>> cigar = "8M2D4M2I3N1M"
        >>> md = "2A5^AG7"
        >>> seq = "ACGTACGTACGTACG"
        >>> cstag.call(cigar, md, seq, is_long=True)
        '=AC*ag=TACGT-ag=ACGT+ac~nn3nn=G'
    """
    cigar, seq = trim_clips(cigar, seq)
    cslong_md = generate_cslong_md(seq, md)
    cslong_md_cigar = generate_cslong_cigar_integrated(cigar, cslong_md)
    cslong_decoded = decode_substitution(cslong_md_cigar)
    cs_tag = "".join(cslong_decoded)
    if is_long is False:
        cs_tag = shorten(cs_tag)
    if prefix is True:
        cs_tag = add_prefix(cs_tag)
    return cs_tag
