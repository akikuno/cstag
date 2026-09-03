from __future__ import annotations

import matplotlib
import pytest

matplotlib.use("Agg")

import cstag
from cstag.to_mutation_percentages import (
    plot_mutation_percentages,
    summarize_cs,
    to_mutation_percentages,
)

SHORT_EXAMPLE_CS_TAGS = [
    "cs:Z::20*ag:15+tt:30-ac:10",
    "cs:Z::20*ag:15+tt:30-ac:10",
]

LONG_EXAMPLE_CS_TAGS = [
    "=ACGT",
    "=AC*gt=T",
    "=C*gt=T",
    "=ACGT",
    "=AC*gt=T",
]


def by_position(records):
    return {record["position"]: record for record in records}


def test_public_api():
    assert cstag.to_mutation_percentages is to_mutation_percentages


def test_short_form_user_example_has_expected_events():
    positions = by_position(summarize_cs(SHORT_EXAMPLE_CS_TAGS))

    assert len(positions) == 78
    assert {record["coverage"] for record in positions.values()} == {2}
    assert positions[21]["substitution_pct"] == 100.0
    assert positions[21]["total_pct"] == 100.0
    assert positions[36]["insertion_pct"] == 100.0
    assert positions[36]["total_pct"] == 100.0
    assert positions[67]["deletion_pct"] == 100.0
    assert positions[68]["deletion_pct"] == 100.0
    assert [
        position for position, record in positions.items() if record["total_pct"]
    ] == [
        21,
        36,
        67,
        68,
    ]


def test_long_form_example_has_expected_substitution_percentages():
    positions = by_position(summarize_cs(LONG_EXAMPLE_CS_TAGS))

    assert len(positions) == 4
    assert positions[2]["coverage"] == 5
    assert positions[2]["substitution_pct"] == 20.0
    assert positions[3]["substitution_pct"] == 40.0
    assert positions[4]["coverage"] == 4


def test_total_is_read_union_when_categories_overlap():
    cs_tags = [
        "cs:Z::2*ag+tt:4-ac:1",
        "cs:Z::2*ag:7",
        "cs:Z::3+g:7",
        "cs:Z::7-ac:1",
    ]
    positions = by_position(summarize_cs(cs_tags))

    assert positions[3]["substitution_pct"] == 50.0
    assert positions[3]["insertion_pct"] == 50.0
    assert positions[3]["total_pct"] == 75.0
    for position in (8, 9):
        assert positions[position]["deletion_pct"] == 50.0
        assert positions[position]["total_pct"] == 50.0


def test_variable_lengths_use_position_specific_coverage():
    positions = by_position(summarize_cs([":5", ":7*ag:2", ":10"]))

    assert positions[5]["coverage"] == 3
    assert positions[8]["coverage"] == 2
    assert positions[8]["substitution_pct"] == 50.0


def test_repeated_same_category_event_is_counted_once_per_tag():
    positions = by_position(summarize_cs([":3+a+t:2", ":5"]))

    assert positions[3]["insertion_pct"] == 50.0
    assert positions[3]["total_pct"] == 50.0


@pytest.mark.parametrize(
    ("cs_tags", "error_type"),
    [
        ([], ValueError),
        ("cs:Z::5", TypeError),
        ([None], TypeError),
        ([""], ValueError),
        (["cs:Z:"], ValueError),
        ([":0"], ValueError),
        ([":2=AC"], ValueError),
        (["=AC:2"], ValueError),
        (["=acgt"], ValueError),
        ([":2*az:2"], ValueError),
        ([":2+TT:2"], ValueError),
        ([":2cs:Z::3"], ValueError),
        ([":2~gt3ag:2"], ValueError),
        (["+tt:5"], ValueError),
    ],
)
def test_invalid_or_unsupported_inputs_raise(cs_tags, error_type):
    with pytest.raises(error_type):
        summarize_cs(cs_tags)


def test_plot_has_four_ordered_filled_bar_panels(tmp_path):
    records = summarize_cs([":2*ag+tt:2", ":5"])
    output_path = tmp_path / "profile.png"
    figure, axes = plot_mutation_percentages(records, output_path)

    assert len(axes) == 4
    assert [axis.get_title() for axis in axes] == [
        "Total mutations",
        "Insertions",
        "Deletions",
        "Substitutions",
    ]
    assert all(axis.get_ylabel() == "Mutation (%)" for axis in axes)
    assert axes[-1].get_xlabel() == "Reference position (1-based)"
    assert all(axis.get_ylim() == pytest.approx((0.0, 100.0)) for axis in axes)
    assert axes[-1].get_xlim() == pytest.approx((0.5, 5.5))
    assert [bar.get_height() for bar in axes[0].patches] == [
        0.0,
        0.0,
        50.0,
        0.0,
        0.0,
    ]
    assert all(bar.get_width() == 1.0 for axis in axes for bar in axis.patches)
    assert output_path.is_file()

    import matplotlib.pyplot as plt

    plt.close(figure)


def test_plot_adds_bottom_region_track(tmp_path):
    records = summarize_cs([":40"])
    regions = [
        {"name": "hoge", "start": 10, "end": 20, "color": "orange"},
        {"name": "fuga", "start": 20, "end": 30, "color": "skyblue"},
    ]
    output_path = tmp_path / "annotated_profile.png"
    figure, axes = plot_mutation_percentages(records, output_path, regions=regions)

    assert len(axes) == 5
    region_axis = axes[-1]
    assert [label.get_text() for label in region_axis.get_yticklabels()] == [
        "hoge",
        "fuga",
    ]
    assert [bar.get_x() for bar in region_axis.patches] == [9.5, 19.5]
    assert [bar.get_width() for bar in region_axis.patches] == [11, 11]
    assert region_axis.get_ylabel() == "Regions"
    assert region_axis.get_xlabel() == "Reference position (1-based)"
    assert output_path.is_file()

    import matplotlib.pyplot as plt

    plt.close(figure)


@pytest.mark.parametrize(
    ("regions", "error_type"),
    [
        ("hoge", TypeError),
        (["hoge"], TypeError),
        ([{"name": "hoge", "start": 1, "end": 2}], ValueError),
        ([{"name": "hoge", "start": 0, "end": 2, "color": "orange"}], ValueError),
        ([{"name": "hoge", "start": 2, "end": 1, "color": "orange"}], ValueError),
        ([{"name": "hoge", "start": 1, "end": 6, "color": "orange"}], ValueError),
        (
            [{"name": "hoge", "start": 1, "end": 2, "color": "not-a-color"}],
            ValueError,
        ),
    ],
)
def test_invalid_regions_raise(regions, error_type):
    records = summarize_cs([":5"])
    with pytest.raises(error_type):
        plot_mutation_percentages(records, regions=regions)


def test_to_mutation_percentages_writes_png_and_returns_report(tmp_path):
    output_path = tmp_path / "profile.png"
    regions = [{"name": "coding", "start": 2, "end": 3, "color": "skyblue"}]

    records = to_mutation_percentages(
        LONG_EXAMPLE_CS_TAGS,
        output_path,
        regions=regions,
    )

    assert len(records) == 4
    assert by_position(records)[2]["substitution_pct"] == 20.0
    assert by_position(records)[3]["substitution_pct"] == 40.0
    assert output_path.is_file()


def test_to_mutation_percentages_writes_editable_pdf(tmp_path):
    output_path = tmp_path / "profile.pdf"

    to_mutation_percentages(LONG_EXAMPLE_CS_TAGS, output_path)

    pdf = output_path.read_bytes()
    assert pdf.startswith(b"%PDF-")
    assert b"/FontFile2" in pdf


def test_to_mutation_percentages_requires_pathlib_path():
    with pytest.raises(TypeError, match=r"pathlib\.Path"):
        to_mutation_percentages(LONG_EXAMPLE_CS_TAGS, "profile.png")
