import re

def to_html(CSTAG: str, OUTPUT_FILE_NAME: str, DESCRIPTION: str = "") -> None:
    """Convert long format of cs tag into short format
    Args:
        CSTAG (str): cs tag in the **long** format
        OUTPUT_FILE_NAME (str): output file name
        DESCRIPTION (str): (optional) header information in the output file
    Return:
        HTML file (*OUTPUT_FILE_NAME.html*)
    Example:
        >>> import cstag
        >>> CSTAG = "cs:Z:=AC+GGG=T-ACGT*at~gt10cg=GNNN"
        >>> OUTPUT = "Report"
        >>> DESCRIPTION = "Example"
        >>> cstag.to_html(CSTAG, OUTPUT, DESCRIPTION)
        https://user-images.githubusercontent.com/15861316/158910398-67f480d2-8742-412a-b528-40e545c46513.png
    """
    import re

    if not re.search(r"[ACGT]", CSTAG):
        raise Exception("Error: cs tag must be a long format")

    html_header = """<!DOCTYPE html>
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

    html_legend ="""
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

    html_footer ="""
    </body>
    </html>
    """

    description = DESCRIPTION
    if description:
        description = f"<h1>{description}</h1>"

    cs = CSTAG.replace("cs:Z:", "")
    list_cs = re.split(r'([-+*~=])', cs)[1:]
    list_cs = [i+j for i,j in zip(list_cs[0::2], list_cs[1::2])]

    html_cs = []
    for cs in list_cs:
        if cs[0] == "=":
            cs = re.sub(r"(N+)", r"<span class='Unknown'>\1</span>", cs)
            html_cs.append(cs[1:])
        elif cs[0] == "*":
            html_cs.append(f"<span class='Sub'>{cs[2].upper()}</span>")
        elif cs[0] == "+":
            html_cs.append(f"<span class='Ins'>{cs[1:].upper()}</span>")
        elif cs[0] == "-":
            html_cs.append(f"<span class='Del'>{cs[1:].upper()}</span>")
        elif cs[0] == "~":
            left = cs[1:3].upper()
            splice = "-" * int(cs[3:-2])
            right = cs[-2:].upper()
            html_cs.append(f"<span class='Splice'>{left + splice + right}</span>")


    html_cs = "".join(html_cs)
    html_cs = f"<p class='p_seq'>{html_cs}</p>"

    report = "\n".join([
        html_header,
        description,
        html_legend,
        html_cs,
        html_footer,
    ])

    with open(OUTPUT_FILE_NAME + '.html', 'w') as f:
        f.write(report)
