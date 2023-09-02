from pathlib import Path
from src.cstag import to_html


def test_html():
    cs_tag = "=AC+GGG=T-ACGT*at~gt10cg=GNNN"
    description = "Example"
    cs_html = to_html(cs_tag, description)
    test = [h for h in cs_html.split("\n") if h.count("<p class='p_seq'>")]
    test = test[0].split()
    answer = Path("tests", "data", "to_html", "report.html").read_text().split("\n")
    answer = [h for h in answer if h.count(r"<p class='p_seq'>")]
    answer = answer[0].split()
    assert test == answer


def test_html_repeat_substitution():
    cs_tag = "=A*at*ag=A"
    description = "Example"
    cs_html = to_html(cs_tag, description)
    test = [h for h in cs_html.split("\n") if h.count("<p class='p_seq'>")]
    test = test[0].split()
    answer = Path("tests", "data", "to_html", "report_substitution.html").read_text().split("\n")
    answer = [h for h in answer if h.count(r"<p class='p_seq'>")]
    answer = answer[0].split()
    assert test == answer


def test_html_repeat_substitution_start():
    cs_tag = "*at*ag=A"
    description = "Example"
    cs_html = to_html(cs_tag, description)
    test = [h for h in cs_html.split("\n") if h.count("<p class='p_seq'>")]
    test = test[0].split()
    answer = Path("tests", "data", "to_html", "report_substitution_start.html").read_text().split("\n")
    answer = [h for h in answer if h.count(r"<p class='p_seq'>")]
    answer = answer[0].split()
    assert test == answer


def test_html_repeat_substitution_end():
    cs_tag = "=A*at*ag"
    description = "Example"
    cs_html = to_html(cs_tag, description)
    test = [h for h in cs_html.split("\n") if h.count("<p class='p_seq'>")]
    test = test[0].split()
    answer = Path("tests", "data", "to_html", "report_substitution_end.html").read_text().split("\n")
    answer = [h for h in answer if h.count(r"<p class='p_seq'>")]
    answer = answer[0].split()
    assert test == answer


def test_html_start_from_N():
    cs_tag = "=NNN=AC+GGG=T-ACGT*at~gt10cg=GNNN"
    description = "Example"
    cs_html = to_html(cs_tag, description)
    test = [h for h in cs_html.split("\n") if h.count("<p class='p_seq'>")]
    test = test[0].split()
    answer = [
        "<p",
        "class='p_seq'><span",
        "class='Unknown'>NNN</span>AC<span",
        "class='Ins'>GGG</span>T<span",
        "class='Del'>ACGT</span><span",
        "class='Sub'>T</span><span",
        "class='Splice'>GT----------CG</span>G<span",
        "class='Unknown'>NNN</span></p>",
    ]
    assert test == answer


def test_html_deletion_plus_N():
    cs_tag = "=T-ACGTNNN=G"
    description = "Example"
    cs_html = to_html(cs_tag, description)
    test = [h for h in cs_html.split("\n") if h.count("<p class='p_seq'>")]
    test = test[0]
    answer = "<p class='p_seq'>T<span class='Del'>ACGT</span><span class='Unknown'>NNN</span>G</p>"
    assert test == answer


def test_html_N_within_deletions():
    cs_tag = "=T-ACGTNNN-ACGT=G"
    description = "Example"
    cs_html = to_html(cs_tag, description)
    test = [h for h in cs_html.split("\n") if h.count("<p class='p_seq'>")][0]
    answer = "<p class='p_seq'>T<span class='Del'>ACGT</span><span class='Unknown'>NNN</span><span class='Del'>ACGT</span>G</p>"
    assert test == answer


def test_html_N_within_insertions():
    cs_tag = "=T+ACGTNNN+ACGT=G"
    description = "Example"
    cs_html = to_html(cs_tag, description)
    test = [h for h in cs_html.split("\n") if h.count("<p class='p_seq'>")][0]
    answer = "<p class='p_seq'>T<span class='Ins'>ACGT</span><span class='Unknown'>NNN</span><span class='Ins'>ACGT</span>G</p>"
    assert test == answer
