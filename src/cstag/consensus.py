from __future__ import annotations

import re
from itertools import chain
from collections import deque, Counter

from cstag.utils.validator import validate_long_format


def split_cs_tags(cs_tags: list[str]) -> list[deque[str]]:
    """
    Split and process each cs tag in cs_tags.

    Args:
        cs_tags (list[str]): list of cs tags in the long format.

    Returns:
        list[deque[str]]: list of processed cs tags as deque objects.
    """
    cs_tags_splitted = []
    for cs_tag in cs_tags:
        # Remove the prefix "cs:Z:" if present
        cs_tag = cs_tag.replace("cs:Z:", "")
        # Split the cs tag using special symbols (-, *, ~, =)
        split_tags = re.split(r"([-*~=])", cs_tag)[1:]
        # Combine the symbol with the corresponding sequence
        combined_tags = [symbol + seq for symbol, seq in zip(split_tags[0::2], split_tags[1::2])]
        # Remove the "=" symbols, as they are not needed for further processing
        cleaned_tags = [tag.replace("=", "") for tag in combined_tags]
        # Further split the tags by the base letters (A, C, G, T)
        further_split_tags = [re.split(r"(?=[ACGT])", tag) for tag in cleaned_tags]
        # Remove any empty strings generated by the split
        non_empty_tags = [[elem for elem in tag if elem] for tag in further_split_tags]
        # Flatten the list of lists into a single list
        flat_tags = list(chain.from_iterable(non_empty_tags))
        cs_tags_splitted.append(deque(flat_tags))
    return cs_tags_splitted


def normalize_read_lengths(cs_list: list[deque[str]], starts: list[int]) -> list[deque[str]]:
    """
    Normalize the lengths of each read in cs_list based on their starts positions.

    Args:
        cs_list (list[deque[str]]): list of deques representing the reads.
        starts (list[int]): Starting positions of each read.

    Returns:
        list[deque[str]]: list of deques representing the reads, now normalized to the same length.
    """
    cs_maxlen = max(len(cs) + start for cs, start in zip(cs_list, starts))

    for i, start in enumerate(starts):
        if start > 0:
            cs_list[i].extendleft(["N"] * start)
        if len(cs_list[i]) < cs_maxlen:
            cs_list[i].extend(["N"] * (cs_maxlen - len(cs_list[i])))

    return cs_list


def get_consensus(cs_list: list[deque[str]]) -> str:
    cs_consensus = []
    for cs in zip(*cs_list):
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
        =AC*gt=T
    """
    if not (len(cs_tags) == len(positions) > 0):
        raise ValueError("Element numbers of each argument must be the same")

    for cs_tag in cs_tags:
        validate_long_format(cs_tag)

    cs_tag_split = split_cs_tags(cs_tags)

    positions_zero_indexed = [pos - 1 for pos in positions]

    cs_tags_normalized_length = normalize_read_lengths(cs_tag_split, positions_zero_indexed)

    cs_consensus = get_consensus(cs_tags_normalized_length)

    return f"cs:Z:{cs_consensus}" if prefix else cs_consensus
