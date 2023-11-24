from __future__ import annotations

import re
from itertools import chain
from collections import deque, Counter

from cstag.utils.validator import validate_cs_tag, validate_long_format


def split_deletion(cs_tag: str) -> list[str]:
    match = re.match(r"-(?P<nucleotides>[acgtn]+)$", cs_tag)
    if match:
        nucleotides = match.group("nucleotides")
        return [f"-{n}" for n in nucleotides]
    return [cs_tag]


def expand_deletion_tags(tags_combined: list[str]) -> list[str]:
    cs_tags_expand_deletion = []
    for tag in tags_combined:
        for tag_splitted in split_deletion(tag):
            cs_tags_expand_deletion.append(tag_splitted)
    return cs_tags_expand_deletion


def split_cs_tags(cs_tags: list[str]) -> list[list[str]]:
    """
    Split and process each cs tag in cs_tags.

    Args:
        cs_tags (list[str]): list of cs tags in the long format.

    Returns:
        list[list[str]]: list of processed cs tags.
    """
    cs_tags_splitted = []
    for cs_tag in cs_tags:
        # Remove the prefix "cs:Z:" if present
        cs_tag = cs_tag.replace("cs:Z:", "")

        # Split the cs tag using special symbols (-, *, ~, =)
        # insertion symbol (+) is ignored because it is not observed in reference sequence
        tags_splitted = re.split(r"([-*~=])", cs_tag)[1:]
        # Combine the symbol with the corresponding sequence
        tags_combined = [symbol + seq for symbol, seq in zip(tags_splitted[0::2], tags_splitted[1::2])]
        tags_combined = expand_deletion_tags(tags_combined)

        # Remove the "=" symbols, as they are not needed for further processing
        cleaned_tags = [tag.replace("=", "") for tag in tags_combined]
        # Further split the tags by the base letters (A, C, G, T)
        further_tags_splitted = [re.split(r"(?=[ACGT])", tag) for tag in cleaned_tags]
        # Remove any empty strings generated by the split
        non_empty_tags = [[elem for elem in tag if elem] for tag in further_tags_splitted]
        # Flatten the list of lists into a single list
        flat_tags = list(chain.from_iterable(non_empty_tags))
        cs_tags_splitted.append(flat_tags)
    return cs_tags_splitted


def normalize_positions(positions: list[int]) -> list[int]:
    """
    Normalize the positions in the given list by shifting them so that the minimum position becomes zero.
    """
    pos_min = min(positions)
    return [pos - pos_min for pos in positions]


def normalize_read_lengths(cs_tags: list[str], positions: list[int]) -> list[list[str]]:
    """
    Normalize the lengths of each read in cs_tags based on their starts positions. If the length is insufficient, fill in with `None`.

    Args:
        cs_tags (list[str]): list of cs tags.
        positions (list[int]): Starting positions of each read.

    Returns:
        list[list[str]]: list of lists representing the reads, now normalized to the same length.
    """
    cs_tags_split = split_cs_tags(cs_tags)
    cs_tags_deque = [deque(cs) for cs in cs_tags_split]
    positions_normalized = normalize_positions(positions)
    cs_maxlen = max(len(cs) + pos for cs, pos in zip(cs_tags_deque, positions_normalized))

    for i, pos in enumerate(positions_normalized):
        if pos > 0:
            cs_tags_deque[i].extendleft([None] * pos)
        if len(cs_tags_deque[i]) < cs_maxlen:
            cs_tags_deque[i].extend([None] * (cs_maxlen - len(cs_tags_deque[i])))
    cs_tags = [list(cs) for cs in cs_tags_deque]
    return cs_tags


def condense_deletions(s: str) -> str:
    # Pattern for detecting continuous nucleotide deletions
    pattern = r"(-[acgtn])+"

    # Function to replace the matched pattern
    def replacement(match) -> str:
        # Remove hyphens and concatenate the nucleotides
        condensed_nucleotides = match.group(0).replace("-", "")
        return f"-{condensed_nucleotides}"

    # Use the regular expression to substitute the pattern with its condensed form
    return re.sub(pattern, replacement, s)


def get_consensus(cs_tags: list[list[str]]) -> str:
    cs_consensus = []
    for cs in zip(*cs_tags):
        # Remove the None that is compensating for the insufficient lead length.
        cs = [c for c in cs if c]
        # Get the most common cs tag(s)
        most_common_tags = Counter(cs).most_common()

        # If there's a unique most common tag, return it
        most_common_tag, _ = most_common_tags[0]
        if len(most_common_tags) == 1 or most_common_tags[0][1] != most_common_tags[1][1]:
            cs_consensus.append(most_common_tag)
            continue
        # If the most common tag is not unique (multimodal), return the first *mutated* mode
        for tag, _ in most_common_tags:
            if not re.search(r"[ACGT]", tag):
                cs_consensus.append(tag)

    cs_consensus = "".join(cs_consensus)
    cs_consensus = condense_deletions(cs_consensus)
    # Append "=" to [ACGTN]
    return re.sub(r"([ACGTN]+)", r"=\1", cs_consensus)


###########################################################
# main
###########################################################


def consensus(cs_tags: list[str], positions: list[int], prefix: bool = False) -> str:
    """generate consensus of cs tags
    Args:
        cs_tags (list): cs tags in the **long** format
        positions (list): 1-based leftmost mapping position (4th column in SAM file)
        prefix (bool, optional): Whether to add the prefix 'cs:Z:' to the cs tag. Defaults to False
    Return:
        str: a consensus of cs tag in the **long** format
    Example:
        >>> import cstag
        >>> cs_tags = ["=ACGT", "=AC*gt=T", "=C*gt=T", "=C*gt=T", "=ACT+ccc=T"]
        >>> positions = [1,1,1,2,1]
        >>> cstag.consensus(cs_tags, positions)
        '=AC*gt=T'
    """
    if not (len(cs_tags) == len(positions) > 0):
        raise ValueError("Element numbers of each argument must be the same")

    for cs_tag in cs_tags:
        validate_cs_tag(cs_tag)
        validate_long_format(cs_tag)

    cs_tags_normalized_length = normalize_read_lengths(cs_tags, positions)

    cs_consensus = get_consensus(cs_tags_normalized_length)

    return f"cs:Z:{cs_consensus}" if prefix else cs_consensus
