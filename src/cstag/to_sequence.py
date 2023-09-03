from __future__ import annotations

from cstag.split import split
from cstag.utils.validator import validate_cs_tag, validate_long_format


def to_sequence(cs_tag: str) -> str:
    validate_cs_tag(cs_tag)
    validate_long_format(cs_tag)

    cs_tag = cs_tag.replace("cs:Z:", "")
    sequence = []
    for cs in split(cs_tag):
        if cs.startswith("="):
            sequence.append(cs[1:].upper())
        elif cs.startswith("+"):
            sequence.append(cs[1:].upper())
        elif cs.startswith("*"):
            sequence.append(cs[-1].upper())

    return "".join(sequence)
