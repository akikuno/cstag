from pathlib import Path
from src.cstag.split import split
from src.cstag.to_html import append_mark_to_n, to_html


def test_append_mark_to_n():
    assert append_mark_to_n("=NACGT") == "@N=ACGT"
    assert append_mark_to_n("=NNNACGT") == "@NNN=ACGT"
    assert append_mark_to_n("=ACGTNNN") == "=ACGT@NNN"
    assert append_mark_to_n("=ACGTNNNACGT") == "=ACGT@NNN=ACGT"
    assert append_mark_to_n("") == ""
    assert append_mark_to_n("=N") == "@N"
    assert append_mark_to_n("=ACGT") == "=ACGT"
    assert append_mark_to_n("=ANA") == "=A@N=A"
    assert append_mark_to_n("=NAN") == "@N=A@N"


def test_split_cstag():
    assert split("@N=ACGT") == ["@N", "=ACGT"]
    assert split("@NNN=ACGT") == ["@NNN", "=ACGT"]
    assert split("=ACGT@NNN") == ["=ACGT", "@NNN"]
    assert split("=ACGT@NNN=ACGT") == ["=ACGT", "@NNN", "=ACGT"]
    assert split("=ACGT@NNN-acgt") == ["=ACGT", "@NNN", "-acgt"]
    assert split("=ACGT@NNN+acgt") == ["=ACGT", "@NNN", "+acgt"]
    assert split("=ACGT@NNN*ac=GT") == ["=ACGT", "@NNN", "*ac", "=GT"]
    assert split("") == []
    assert split("@N") == ["@N"]
    assert split("=ACGT") == ["=ACGT"]


###########################################################
# main
###########################################################


def test_html():
    cs_tag = "=AC+ggg=T-acgt*at~gt10ag=GNNN"
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
    cs_tag = "=NNN=AC+ggg=T-acgt*at~gt10cg=GNNN"
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
        "class='Splice'>GT------CG</span>G<span",
        "class='Unknown'>NNN</span></p>",
    ]
    assert test == answer


def test_html_deletion_with_N():
    cs_tag = "=T-acgt=NNNG"
    description = "Example"
    cs_html = to_html(cs_tag, description)
    test = [h for h in cs_html.split("\n") if h.count("<p class='p_seq'>")]
    test = test[0]
    answer = "<p class='p_seq'>T<span class='Del'>ACGT</span><span class='Unknown'>NNN</span>G</p>"
    assert test == answer


def test_html_N_within_deletions():
    cs_tag = "=T-acgt=NNN-acgt=G"
    description = "Example"
    cs_html = to_html(cs_tag, description)
    test = [h for h in cs_html.split("\n") if h.count("<p class='p_seq'>")][0]
    answer = "<p class='p_seq'>T<span class='Del'>ACGT</span><span class='Unknown'>NNN</span><span class='Del'>ACGT</span>G</p>"
    assert test == answer


def test_html_N_within_insertions():
    cs_tag = "=T+acgt=NNN+acgt=G"
    description = "Example"
    cs_html = to_html(cs_tag, description)
    test = [h for h in cs_html.split("\n") if h.count("<p class='p_seq'>")][0]
    answer = "<p class='p_seq'>T<span class='Ins'>ACGT</span><span class='Unknown'>NNN</span><span class='Ins'>ACGT</span>G</p>"
    assert test == answer
