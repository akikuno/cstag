from __future__ import annotations

from cstag.shorten import shorten


###########################################################
# Trim soft and hard clips from the CIGAR and sequence
###########################################################


def parse_cigar(cigar: str) -> list[tuple[str, int]]:
    """
    Parse a CIGAR string into a list of tuples containing operation and length.
    """
    parsed_cigar = []
    start_idx = 0
    for idx, operation in enumerate(cigar):
        if operation.isdigit():
            continue
        length = int(cigar[start_idx:idx])
        parsed_cigar.append((operation, length))
        start_idx = idx + 1
    return parsed_cigar


def parse_md(md: str) -> list[tuple[str, int]]:
    """
    Parse an MD tag into a list of tuples containing operation and length.
    """
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


def join_cigar(cigar_tuples: list[tuple[str, int]]) -> str:
    return "".join(f"{length}{operation}" for operation, length in cigar_tuples)


def trim_clips(cigar: str, seq: str) -> tuple[str, str]:
    if all(x not in cigar for x in "SH"):
        return cigar, seq
    parsed_cigar = parse_cigar(cigar)
    # trim soft clips of cigar and seq
    if parsed_cigar[0][0] == "S":
        length_softclip = parsed_cigar[0][1]
        seq = seq[length_softclip:]
        parsed_cigar = parsed_cigar[1:]
    if parsed_cigar[-1][0] == "S":
        length_softclip = parsed_cigar[-1][1]
        seq = seq[:-length_softclip]
        parsed_cigar = parsed_cigar[:-1]
    # trim hard clips of cigar
    if parsed_cigar[0][0] == "H":
        parsed_cigar = parsed_cigar[1:]
    if parsed_cigar[-1][0] == "H":
        parsed_cigar = parsed_cigar[:-1]
    cigar = join_cigar(parsed_cigar)
    return cigar, seq


###########################################################
# Generate cs tag in long format
###########################################################


def expand_cigar_operations(cigar: str) -> list[str]:
    parsed_cigar = parse_cigar(cigar)
    expanded_list = []
    for op, num in parsed_cigar:
        if op in ["D", "N", "I"]:
            expanded_list.append(op * num)
        else:
            expanded_list.extend([op] * num)
    return expanded_list


def expand_md_operations(md: str) -> list[str]:
    parsed_md = parse_md(md)
    expanded_list = []
    for op, num in parsed_md:
        if op.startswith("^"):
            expanded_list.append(op)
            continue
        expanded_list.extend([op] * num)
    return expanded_list


def remove_consecutive_equals(cs_long: list[str]) -> list[str]:
    if not cs_long:
        return cs_long
    for i, cs in enumerate(cs_long):
        if i == 0:
            prev_op = cs[0]
            continue
        curr_op = cs[0]
        if prev_op == curr_op == "=":
            cs_long[i] = cs[1:]
        else:
            prev_op = cs[0]
    return cs_long


def generate_cs_long(cigar: str, md: str, seq: str) -> str:
    cigar_list = expand_cigar_operations(cigar)
    md_list = expand_md_operations(md)
    idx_cigar, idx_md, idx_seq = 0, 0, 0
    cs_long = []
    while idx_seq < len(seq) and idx_cigar < len(cigar_list) and idx_md < len(md_list):
        if cigar_list[idx_cigar] == "M":
            if md_list[idx_md] == "=":
                cs_long.append(f"={seq[idx_seq]}")
            else:
                cs_long.append(f"*{md_list[idx_md]}{seq[idx_seq]}".lower())
            idx_cigar += 1
            idx_md += 1
            idx_seq += 1
            continue
        if cigar_list[idx_cigar][0] == "D":
            cs_long.append(md_list[idx_md].replace("^", "-").lower())
            idx_cigar += 1
            idx_md += 1
            continue
        if cigar_list[idx_cigar][0] == "I":
            num_insertion = len(cigar_list[idx_cigar])
            seq_insertion = "".join(seq[idx_seq : idx_seq + num_insertion])
            cs_long.append(f"+{seq_insertion}".lower())
            idx_cigar += 1
            idx_seq += num_insertion
            continue
        if cigar_list[idx_cigar][0] == "N":
            cs_long.append(f"~nn{len(cigar_list[idx_cigar])}nn")
            idx_cigar += 1
            continue
    return "".join(remove_consecutive_equals(cs_long))


def add_prefix(cs_tag: str) -> str:
    return f"cs:Z:{cs_tag}"


###########################################################
# main
###########################################################


def call(cigar: str, md: str, seq: str, long: bool = False, prefix: bool = False) -> str:
    """
    Generate a cs tag based on CIGAR, MD, and SEQ information.

    Args:
        cigar (str): CIGAR string representing the alignment.
        md (str): MD tag representing mismatching positions/base.
        seq (str): The sequence of the read.
        long (bool, optional): Whether to return the cs tag in long format. Defaults to False.
        prefix (bool, optional): Whether to add the prefix 'cs:Z:' to the cs tag. Defaults to False

    Returns:
        str: A cs tag representing the alignment and differences.

    Example:
        >>> import cstag
        >>> cigar = "8M2D4M2I3N1M"
        >>> md = "2A5^AG7"
        >>> seq = "ACGTACGTACGTACG"
        >>> cstag.call(cigar, md, seq, long=True)
        '=AC*ag=TACGT-ag=ACGT+ac~nn3nn=G'
    """
    cigar, seq = trim_clips(cigar, seq)
    cs_tag = generate_cs_long(cigar, md, seq)
    if long is False:
        cs_tag = shorten(cs_tag)
    if prefix is True:
        cs_tag = add_prefix(cs_tag)
    return cs_tag
