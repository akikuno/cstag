from __future__ import annotations

from pathlib import Path
from weasyprint import HTML
from cstag.to_html import to_html


def to_pdf(cs_tag: str, description: str, path_out: str | Path) -> None:
    """
    Convert a cs tag and its description to a PDF file.

    This function takes a cs (custom string) tag and its description, converts
    it to HTML using the `to_html` function, and then writes it to a PDF file
    using WeasyPrint.

    Args:
        cs_tag (str): The cs tag to be converted.
        description (str): The description associated with the cs tag.
        path_out (str | Path): The path where the output PDF file will be saved.

    Returns:
        None: This function does not return anything.

    Examples:
        >>> import cstag
        >>> cs_tag = "=AC+ggg=T-acgt*at~gt10cg=GNNN"
        >>> description = "Example"
        >>> path_out = "report.pdf"
        >>> to_pdf(cs_tag, description, path_out)
    """
    cs_tag_html = to_html(cs_tag, description)
    HTML(string=cs_tag_html).write_pdf(path_out)
