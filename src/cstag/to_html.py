import re

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


def validate_cstag(cstag: str) -> None:
    if not re.search(r"[ACGTN]", cstag):
        raise Exception("Error: cs tag must be a long format")


def process_cstag(cstag: str) -> str:
    cstag = cstag.replace("cs:Z:", "")
    cstag_split_n = re.split(r"(N+)", cstag)
    cs_mark_n = "".join(["@" + cs if cs.startswith("N") else cs for cs in cstag_split_n])
    list_cs = re.split(r"([-+*~=@])", cs_mark_n)
    list_cs = [l for l in list_cs if l != ""]
    list_cs = [i + j for i, j in zip(list_cs[0::2], list_cs[1::2])]
    html_cs = []
    idx = 0
    while idx < len(list_cs):
        cs = list_cs[idx]
        if cs.startswith("="):
            html_cs.append(cs[1:])
        elif cs.startswith("@"):
            cs = re.sub(r"(N+)", r"<span class='Unknown'>\1</span>", cs[1:])
            html_cs.append(cs)
        elif cs[0] == "*":
            html_cs.append(f"<span class='Sub'>{cs[2].upper()}")
            while idx < len(list_cs) - 1 and list_cs[idx + 1].startswith("*"):
                html_cs.append(f"{list_cs[idx+1][2].upper()}")
                idx += 1
            html_cs.append("</span>")
        elif cs[0] == "+":
            html_cs.append(f"<span class='Ins'>{cs[1:].upper()}</span>")
        elif cs[0] == "-":
            html_cs.append(f"<span class='Del'>{cs[1:].upper()}</span>")
        elif cs[0] == "~":
            left = cs[1:3].upper()
            splice = "-" * int(cs[3:-2])
            right = cs[-2:].upper()
            html_cs.append(f"<span class='Splice'>{left + splice + right}</span>")
        idx += 1
    html_cs = "".join(html_cs)
    return f"<p class='p_seq'>{html_cs}</p>"


def to_html(cstag: str, description: str = "") -> str:
    """Output HTML string showing a sequence with mutations colored
    Args:
        cstag (str): cs tag in the **long** format
        description (str): (optional) header information in the output string
    Return:
        HTML string
    Example:
        >>> import cstag
        >>> cstag = "cs:Z:=AC+GGG=T-ACGT*at~gt10cg=GNNN"
        >>> description = "Example"
        >>> html_string = cstag.to_html(cstag, description)
    """
    validate_cstag(cstag)
    description_str = f"<h1>{description}</h1>" if description else ""
    html_cs = process_cstag(cstag)
    report = "\n".join(
        [
            HTML_HEADER,
            description_str,
            HTML_LEGEND,
            html_cs,
            HTML_FOOTER,
        ]
    )
    return report
