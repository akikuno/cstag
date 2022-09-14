from pathlib import Path
from src.cstag import to_html


def test_html():
    cs = "cs:Z:=AC+GGG=T-ACGT*at~gt10cg=GNNN"
    description = "Example"
    cs_html = to_html(cs, description)
    test = [h for h in cs_html.split("\n") if h.count("<p class='p_seq'>")]
    test = test[0].split()
    answer = Path("tests", "data", "to_html", "report.html").read_text().split("\n")
    answer = [h for h in answer if h.count(r"<p class='p_seq'>")]
    answer = answer[0].split()
    assert test == answer


def test_html_repeat_substitution():
    cs = "cs:Z:=A*at*ag=A"
    description = "Example"
    cs_html = to_html(cs, description)
    test = [h for h in cs_html.split("\n") if h.count("<p class='p_seq'>")]
    test = test[0].split()
    answer = Path("tests", "data", "to_html", "report_substitution.html").read_text().split("\n")
    answer = [h for h in answer if h.count(r"<p class='p_seq'>")]
    answer = answer[0].split()
    assert test == answer


def test_html_repeat_substitution_start():
    cs = "cs:Z:*at*ag=A"
    description = "Example"
    cs_html = to_html(cs, description)
    test = [h for h in cs_html.split("\n") if h.count("<p class='p_seq'>")]
    test = test[0].split()
    answer = Path("tests", "data", "to_html", "report_substitution_start.html").read_text().split("\n")
    answer = [h for h in answer if h.count(r"<p class='p_seq'>")]
    answer = answer[0].split()
    assert test == answer


def test_html_repeat_substitution_end():
    cs = "cs:Z:=A*at*ag"
    description = "Example"
    cs_html = to_html(cs, description)
    test = [h for h in cs_html.split("\n") if h.count("<p class='p_seq'>")]
    test = test[0].split()
    answer = Path("tests", "data", "to_html", "report_substitution_end.html").read_text().split("\n")
    answer = [h for h in answer if h.count(r"<p class='p_seq'>")]
    answer = answer[0].split()
    assert test == answer

