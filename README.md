[![Licence](https://img.shields.io/badge/License-MIT-9cf.svg?style=flat-square)](https://choosealicense.com/licenses/mit/)
[![Docs](https://img.shields.io/badge/Docs-passing-informational.svg?style=flat-square&color=brightgreen)](https://akikuno.github.io/cstag/cstag/)
[![Test](https://img.shields.io/github/workflow/status/akikuno/cstag/Pytest?json&label=Test&color=brightgreen&style=flat-square)](https://github.com/akikuno/cstag/actions)
[![Python](https://img.shields.io/pypi/pyversions/cstag.svg?label=Python&color=blue&style=flat-square)](https://pypi.org/project/cstag/)
[![PyPI](https://img.shields.io/pypi/v/cstag.svg?label=PyPI&color=orange&style=flat-square)](https://pypi.org/project/cstag/)
<!-- [![Bioconda](https://img.shields.io/badge/Install%20with-Bioconda-brightgreen.svg)](https://anaconda.org/bioconda/cstag) -->

# cstag

`cstag` is a Python module to manipulate [minimap2's CS tag](https://github.com/lh3/minimap2#cs).

- `cstag.shorten()`: to convert a cs tag from long to short format
- `cstag.lengthen()`: to convert a cs tag from short to long format
- `cstag.consensus()`: to generate a consensus cs tag from multiple cs tags
- `cstag.to_html()`: to output html report
<!-- - `cstag.to_mids()`: to convert cs tag into [compressed MIDS format](https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.3001507#:~:text=S6%20Fig.%20Compressed%20MIDS%20conversion.) (under-development:construction_worker:) -->

## Installation

From [PyPI](https://pypi.org/project/cstag/):

```bash
pip install cstag
```

<!-- From [Bioconda](https://anaconda.org/bioconda/cstag)

```bash
conda config --add channels defaults
conda config --add channels conda-forge
conda config --add channels bioconda
conda install -c bioconda cstag
``` -->

## Examples

### Shorten/Lengthen

```python
import cstag

"""
Convert long format of cs tag into short format
"""
cs = "cs:Z:=ACGT*ag=CGT"
cstag.shorten(cs)
# => cs:Z::4*ag:3


"""
Convert short format of cs tag into long format
"""
cs = "cs:Z::4*ag:3"
cigar = "8M"
seq = "ACGTACGT"
cstag.lengthen(cs, cigar, seq)
# => cs:Z:=ACGT*ag=CGT
```

### Call consensus

```python
import cstag
cs_list = ["cs:Z:=ACGT", "cs:Z:=AC*gt=T", "cs:Z:=C*gt=T", "cs:Z:=C*gt=T", "cs:Z:=ACT+ccc=T"]
cigar_list = ["4M", "4M", "1S3M", "3M", "3M3I1M"]
pos_list = [1, 1, 1, 2, 1]
cstag.consensus(cs_list, cigar_list, pos)
# => cs:Z:=AC*gt*T
```

### Output HTML report

```python
import cstag
cs = "cs:Z:=AC+GGG=T-ACGT*at~gt10cg=GNNN"
output = "report"
description = "Example"
cstag.to_html(cs, output, description)
# => Output "report.html"
```
The `report.html` is :point_down:

<img width="414" alt="example_report" src="https://user-images.githubusercontent.com/15861316/158910398-67f480d2-8742-412a-b528-40e545c46513.png">
