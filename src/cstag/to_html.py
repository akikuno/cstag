from __future__ import annotations

import re

from cstag.utils.validator import validate_long_format

HTML_HEADER = """<!DOCTYPE html>
    <html>
    <head>
    <style>
    h1 {
    font-family: Consolas, 'Courier New', monospace;
    color: #333;
    padding: 0.1em 0;
    border-top: solid 3px #333;
    border-bottom: solid 3px #333;
    }
    .p_seq {
    font-family: Consolas, 'Courier New', monospace;
    color: #585858;
    word-wrap: break-word;
    letter-spacing: 0.15em;
    }
    .p_legend {
    font-family: Consolas, 'Courier New', monospace;
    color: #585858;
    word-wrap: break-word;
    }

    .Ins {
    color: #333;
    border: 0.1em solid;
    background-color: #ee827c;
    font-weight: bold;
    # border-radius: 5px;
    }
    .Del {
    color: #333;
    border: 0.1em solid;
    background-color: #a0d8ef;
    font-weight: bold;
    # border-radius: 5px;
    }
    .Sub {
    color: #333;
    border: 0.1em solid;
    background-color: #98d98e;
    font-weight: bold;
    # border-radius: 5px;
    }
    .Splice {
    color: #333;
    border: 0.1em solid;
    background-color: #f8e58c;
    font-weight: bold;
    }
    .Unknown {
    color: #333;
    border: 0.1em solid;
    background-color: #c0c6c9;
    font-weight: bold;
    # border-radius: 5px;
    }

    </style>
    </head>
    <body>
"""

HTML_LEGEND = """
<p class = "p_legend">
Labels:
<span class="Ins">Insertion</span>
<span class="Del">Deletion</span>
<span class="Sub">Substitution</span>
<span class="Splice">Splicing</span>
<span class="Unknown">Unknown</span>
</p>
<hr>
"""

HTML_FOOTER = """
</body>
</html>
"""


def build_html_parts(cs: str, css_class: str) -> str:
    return f"<span class='{css_class}'>{cs.upper()}</span>"


def process_cs_tag(cs_tag: str) -> str:
    # Format cs_tag
    cs_tag = cs_tag.replace("cs:Z:", "")
    cs_tag_split_n = [cs for cs in re.split(r"(N+)", cs_tag) if cs not in ("", "=")]
    cs_tag_mark_n = "".join(["@" + cs if cs.startswith("N") else cs for cs in cs_tag_split_n])
    cs_tag_split = [cs for cs in re.split(r"([-+*~=@])", cs_tag_mark_n) if cs]
    cs_tag_combined = [tag + contents for tag, contents in zip(cs_tag_split[0::2], cs_tag_split[1::2])]
    # Build html
    html_parts = []
    idx = 0
    while idx < len(cs_tag_combined):
        cs = cs_tag_combined[idx]
        if cs.startswith("="):
            html_parts.append(cs[1:])
        elif cs.startswith("@"):
            html_parts.append(build_html_parts(cs[1:], "Unknown"))
        elif cs.startswith("*"):
            substitutions = [cs[2]]
            while idx < len(cs_tag_combined) - 1 and cs_tag_combined[idx + 1].startswith("*"):
                substitutions.append(cs_tag_combined[idx + 1][2])
                idx += 1
            html_parts.append(build_html_parts("".join(substitutions), "Sub"))
        elif cs.startswith("+"):
            html_parts.append(build_html_parts(cs[1:], "Ins"))
        elif cs.startswith("-"):
            html_parts.append(build_html_parts(cs[1:], "Del"))
        elif cs.startswith("~"):
            left, right = cs[1:3], cs[-2:]
            splice = "-" * int(cs[3:-2])
            html_parts.append(build_html_parts(f"{left}{splice}{right}", "Splice"))
        idx += 1

    return f"<p class='p_seq'>{''.join(html_parts)}</p>"


def to_html(cs_tag: str, description: str = "") -> str:
    """Output HTML string showing a sequence with mutations colored
    Args:
        cs_tag (str): cs tag in the **long** format
        description (str): (optional) header information in the output string
    Return:
        HTML string
    Example:
        >>> import cstag
        >>> cs_tag = "=AC+GGG=T-ACGT*at~gt10cg=GNNN"
        >>> description = "Example"
        >>> html_string = cstag.to_html(cs_tag, description)
    """
    validate_long_format(cs_tag)
    description_str = f"<h1>{description}</h1>" if description else ""
    html_parts = process_cs_tag(cs_tag)
    report = "\n".join(
        [
            HTML_HEADER,
            description_str,
            HTML_LEGEND,
            html_parts,
            HTML_FOOTER,
        ]
    )
    return report
