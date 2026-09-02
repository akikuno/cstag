from __future__ import annotations

import re
from collections import defaultdict
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
from matplotlib.colors import is_color_like


CS_PREFIX = "cs:Z:"
CS_TOKEN_PATTERN = re.compile(
    r"=[ACGTN]+|:[0-9]+|\*[acgtn][acgtn]|\+[acgtn]+|-[acgtn]+"
)
PROFILE_KEYS = (
    "position",
    "coverage",
    "total_pct",
    "insertion_pct",
    "deletion_pct",
    "substitution_pct",
)
REGION_KEYS = ("name", "start", "end", "color")


def _tokenize_cs(cs_tag: str, tag_index: int) -> list[str]:
    """Validate and tokenize one minimap2 short- or long-form cs tag."""
    if not isinstance(cs_tag, str):
        raise TypeError(f"cs_tags[{tag_index}] must be a string")

    if cs_tag.startswith(CS_PREFIX):
        normalized = cs_tag[len(CS_PREFIX) :]
        if CS_PREFIX in normalized:
            raise ValueError(
                f"Invalid cs tag at index {tag_index}: repeated cs:Z: prefix"
            )
    else:
        if CS_PREFIX in cs_tag:
            raise ValueError(
                f"Invalid cs tag at index {tag_index}: cs:Z: must be at the start"
            )
        normalized = cs_tag

    if not normalized:
        raise ValueError(f"Invalid cs tag at index {tag_index}: tag is empty")
    if "~" in normalized:
        raise ValueError(
            f"cs_tags[{tag_index}] contains unsupported splice operation '~'"
        )

    tokens = CS_TOKEN_PATTERN.findall(normalized)
    if "".join(tokens) != normalized:
        raise ValueError(f"Invalid cs tag at index {tag_index}: {cs_tag}")
    if any(token.startswith(":") for token in tokens) and any(
        token.startswith("=") for token in tokens
    ):
        raise ValueError(f"cs_tags[{tag_index}] mixes short and long match operations")
    return tokens


def _events_for_tag(
    cs_tag: str, tag_index: int
) -> tuple[set[int], dict[str, set[int]]]:
    """Return covered positions and per-category event positions for one tag."""
    tokens = _tokenize_cs(cs_tag, tag_index)
    reference_position = 1
    coverage: set[int] = set()
    events = {
        "insertion": set(),
        "deletion": set(),
        "substitution": set(),
    }

    for token in tokens:
        operation = token[0]
        if operation in {":", "="}:
            length = int(token[1:]) if operation == ":" else len(token) - 1
            positions = range(reference_position, reference_position + length)
            coverage.update(positions)
            reference_position += length
        elif operation == "*":
            coverage.add(reference_position)
            events["substitution"].add(reference_position)
            reference_position += 1
        elif operation == "+":
            anchor_position = reference_position - 1
            if anchor_position < 1 or anchor_position not in coverage:
                raise ValueError(
                    f"cs_tags[{tag_index}] starts with an insertion that has "
                    "no left reference anchor"
                )
            events["insertion"].add(anchor_position)
        elif operation == "-":
            length = len(token) - 1
            positions = set(range(reference_position, reference_position + length))
            coverage.update(positions)
            events["deletion"].update(positions)
            reference_position += length

    if not coverage:
        raise ValueError(f"cs_tags[{tag_index}] has a reference span of zero")
    return coverage, events


def summarize_cs(cs_tags: Sequence[str]) -> list[dict[str, int | float]]:
    """Calculate mutation percentages at each relative reference position.

    Short- and long-form cs tags are accepted, with or without the ``cs:Z:``
    prefix. All tags are assumed to begin at relative reference position 1.
    Each percentage uses the number of tags covering that position as its
    denominator. ``total_pct`` is the union of reads with any mutation at the
    position, so it cannot exceed 100 percent.

    Args:
        cs_tags: Non-empty sequence of minimap2 cs tag strings.

    Returns:
        One dictionary per 1-based reference position. Each dictionary contains
        ``position``, ``coverage``, ``total_pct``, ``insertion_pct``,
        ``deletion_pct``, and ``substitution_pct``.
    """
    if isinstance(cs_tags, (str, bytes)) or not isinstance(cs_tags, Sequence):
        raise TypeError("cs_tags must be a non-empty sequence of strings")
    if not cs_tags:
        raise ValueError("cs_tags must not be empty")

    coverage_reads: dict[int, set[int]] = defaultdict(set)
    event_reads: dict[str, dict[int, set[int]]] = {
        "insertion": defaultdict(set),
        "deletion": defaultdict(set),
        "substitution": defaultdict(set),
    }

    for tag_index, cs_tag in enumerate(cs_tags):
        coverage, events = _events_for_tag(cs_tag, tag_index)
        for position in coverage:
            coverage_reads[position].add(tag_index)
        for category, positions in events.items():
            for position in positions:
                event_reads[category][position].add(tag_index)

    max_position = max(coverage_reads)
    profile: list[dict[str, int | float]] = []
    for position in range(1, max_position + 1):
        covered = coverage_reads[position]
        coverage_count = len(covered)
        insertion_reads = event_reads["insertion"][position]
        deletion_reads = event_reads["deletion"][position]
        substitution_reads = event_reads["substitution"][position]
        total_reads = insertion_reads | deletion_reads | substitution_reads

        def percentage(reads: set[int]) -> float:
            return 100.0 * len(reads) / coverage_count

        profile.append(
            {
                "position": position,
                "coverage": coverage_count,
                "total_pct": percentage(total_reads),
                "insertion_pct": percentage(insertion_reads),
                "deletion_pct": percentage(deletion_reads),
                "substitution_pct": percentage(substitution_reads),
            }
        )
    return profile


def _validate_regions(
    regions: Sequence[Mapping[str, object]] | None, max_position: int
) -> list[dict[str, str | int]]:
    """Validate optional 1-based inclusive region annotations."""
    if regions is None:
        return []
    if isinstance(regions, (str, bytes)) or not isinstance(regions, Sequence):
        raise TypeError("regions must be a sequence of dictionaries or None")

    validated: list[dict[str, str | int]] = []
    for region_index, region in enumerate(regions):
        if not isinstance(region, Mapping):
            raise TypeError(f"regions[{region_index}] must be a dictionary")
        missing = set(REGION_KEYS) - set(region)
        if missing:
            missing_list = ", ".join(sorted(missing))
            raise ValueError(f"regions[{region_index}] is missing keys: {missing_list}")

        name = region["name"]
        start = region["start"]
        end = region["end"]
        color = region["color"]
        if not isinstance(name, str) or not name:
            raise ValueError(
                f"regions[{region_index}]['name'] must be a non-empty string"
            )
        if isinstance(start, bool) or not isinstance(start, int):
            raise TypeError(f"regions[{region_index}]['start'] must be an integer")
        if isinstance(end, bool) or not isinstance(end, int):
            raise TypeError(f"regions[{region_index}]['end'] must be an integer")
        if not 1 <= start <= end <= max_position:
            raise ValueError(
                f"regions[{region_index}] must satisfy "
                f"1 <= start <= end <= {max_position}"
            )
        if not isinstance(color, str) or not is_color_like(color):
            raise ValueError(f"regions[{region_index}]['color'] is not a valid color")

        validated.append({"name": name, "start": start, "end": end, "color": color})
    return validated


def plot_mutation_percentages(
    records: Sequence[dict[str, int | float]],
    output_path: Path | None = None,
    regions: Sequence[Mapping[str, object]] | None = None,
) -> tuple[Any, Any]:
    """Create four mutation plots and an optional bottom region track."""
    if isinstance(records, (str, bytes)) or not isinstance(records, Sequence):
        raise TypeError("records must be a non-empty sequence of dictionaries")
    if not records:
        raise ValueError("records must not be empty")
    if output_path is not None and not isinstance(output_path, Path):
        raise TypeError("output_path must be a pathlib.Path or None")

    for record_index, record in enumerate(records):
        if not isinstance(record, dict):
            raise TypeError(f"records[{record_index}] must be a dictionary")
        missing = set(PROFILE_KEYS) - set(record)
        if missing:
            missing_list = ", ".join(sorted(missing))
            raise ValueError(f"records[{record_index}] is missing keys: {missing_list}")

    positions = [record["position"] for record in records]
    series = (
        ("total_pct", "Total mutations", "#1f77b4"),
        ("insertion_pct", "Insertions", "#ff7f0e"),
        ("deletion_pct", "Deletions", "#d62728"),
        ("substitution_pct", "Substitutions", "#2ca02c"),
    )
    validated_regions = _validate_regions(regions, int(positions[-1]))
    if validated_regions:
        region_height = max(0.45, 0.22 * len(validated_regions))
        figure, axes = plt.subplots(
            5,
            1,
            figsize=(12, 11 + 0.25 * len(validated_regions)),
            sharex=True,
            constrained_layout=True,
            gridspec_kw={"height_ratios": [1, 1, 1, 1, region_height]},
        )
        mutation_axes = axes[:4]
        region_axis = axes[4]
    else:
        figure, axes = plt.subplots(
            4,
            1,
            figsize=(12, 10),
            sharex=True,
            constrained_layout=True,
        )
        mutation_axes = axes
        region_axis = None

    for axis, (key, title, color) in zip(mutation_axes, series):
        values = [record[key] for record in records]
        axis.bar(
            positions,
            values,
            width=1.0,
            align="center",
            color=color,
            edgecolor="none",
            alpha=0.85,
        )
        axis.set_title(title)
        axis.set_ylabel("Mutation (%)")
        axis.set_ylim(0, 100)
        axis.grid(axis="both", alpha=0.25)

    if region_axis is not None:
        for row, region in enumerate(validated_regions):
            start = int(region["start"])
            end = int(region["end"])
            region_axis.barh(
                row,
                end - start + 1,
                left=start - 0.5,
                height=0.7,
                color=str(region["color"]),
                edgecolor="none",
                alpha=0.85,
            )
        region_axis.set_yticks(
            range(len(validated_regions)),
            labels=[str(region["name"]) for region in validated_regions],
        )
        region_axis.set_ylim(-0.5, len(validated_regions) - 0.5)
        region_axis.invert_yaxis()
        region_axis.set_ylabel("Regions")
        region_axis.grid(axis="x", alpha=0.25)
        x_axis = region_axis
    else:
        x_axis = mutation_axes[-1]

    x_axis.set_xlabel("Reference position (1-based)")
    x_axis.set_xlim(positions[0] - 0.5, positions[-1] + 0.5)

    if output_path is not None:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        if output_path.suffix.lower() == ".pdf":
            # Keep plot elements vector-based and embed editable TrueType text.
            with plt.rc_context({"pdf.fonttype": 42}):
                figure.savefig(output_path, bbox_inches="tight")
        else:
            figure.savefig(output_path, dpi=150, bbox_inches="tight")

    return figure, axes


def to_mutation_percentages(
    cs_tags: Sequence[str],
    output_path: Path,
    regions: Sequence[Mapping[str, object]] | None = None,
) -> list[dict[str, int | float]]:
    """Report and plot mutation percentages at each reference position.

    Args:
        cs_tags: Python sequence containing short- or long-form cs tag strings.
        output_path: Path of the plot file to create. The format is inferred
            from its extension. Use ``.pdf`` for an editable vector PDF with
            embedded TrueType fonts, or ``.png`` for a raster image.
        regions: Optional sequence of dictionaries describing regions to annotate
            below the mutation plots. Each dictionary must contain ``name``
            (the displayed label), ``start`` and ``end`` (1-based, inclusive
            reference positions), and ``color`` (a Matplotlib-compatible color).
            For example::

                [
                    {"name": "crRNA", "start": 80, "end": 99,
                     "color": "lightblue"},
                    {"name": "index", "start": 207, "end": 214,
                     "color": "lightgreen"},
                ]

            Each region is drawn as a separate horizontal bar, so overlapping
            regions remain visible. Supplying one or more regions adds a fifth
            annotation track below the four mutation panels; ``None`` or an
            empty sequence keeps the original four-panel plot.

    Returns:
        One dictionary per 1-based relative reference position containing
        coverage and total, insertion, deletion, and substitution percentages.
    """
    if not isinstance(output_path, Path):
        raise TypeError("output_path must be a pathlib.Path")

    profile = summarize_cs(cs_tags)
    figure, _ = plot_mutation_percentages(profile, output_path, regions=regions)
    plt.close(figure)
    return profile
