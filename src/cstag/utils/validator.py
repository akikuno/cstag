from __future__ import annotations

import re


def validate_short_format(cs_tag: str) -> None:
    if re.search(r"=[ACGTN]+", cs_tag):
        raise ValueError("cs tag must be in short format")


def validate_long_format(cs_tag: str) -> None:
    if re.search(r":[0-9]+", cs_tag):
        raise ValueError("cs tag must be in long format")


def validate_threshold(threshold: int) -> None:
    if not isinstance(threshold, int):
        raise ValueError("threshold must be an integer")

    if not 0 <= threshold <= 40:
        raise ValueError("threshold must be within a range between 0 to 40")
