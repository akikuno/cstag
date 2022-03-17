[![Licence](https://img.shields.io/badge/License-MIT-9cf.svg?style=flat-square)](https://choosealicense.com/licenses/mit/)
[![Docs](https://img.shields.io/badge/Docs-passing-informational.svg?style=flat-square)](https://akikuno.github.io/cstag/cstag/)
[![Python](https://img.shields.io/pypi/pyversions/cstag.svg?label=Python&color=green&style=flat-square)](https://pypi.org/project/cstag/)
[![Test](https://img.shields.io/github/workflow/status/akikuno/cstag/Pytest?json&label=Test&color=orange&style=flat-square)](https://github.com/akikuno/cstag/actions)
[![PyPI](https://img.shields.io/pypi/v/cstag.svg?label=PyPI&color=brightgreen&style=flat-square)](https://pypi.org/project/cstag/)
<!-- [![Bioconda](https://img.shields.io/badge/Install%20with-Bioconda-brightgreen.svg)](https://anaconda.org/bioconda/cstag) -->

# cstag

`cstag` is a Python module to manipulate [minimap2's CS tag](https://github.com/lh3/minimap2#cs).

- `cstag.shorten()`: to convert a cs tag from long to short format
- `cstag.lengthen()`: to convert a cs tag from short to long format
- `cstag.to_consensus()`: to generate a consensus cs tag from multiple cs tags
- `cstag.to_html()`: to output html report (under-development:construction_worker:)
- `cstag.to_mids()`: to convert cs tag into [compressed MIDS format](https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.3001507#:~:text=S6%20Fig.%20Compressed%20MIDS%20conversion.) (under-development:construction_worker:)

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

## Example

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


"""
Generate consensus of multiple cs tags
"""
cs_list = ["cs:Z:=ACGT", "cs:Z:=AC*gt=T", "cs:Z:=C*gt=T", "cs:Z:=C*gt=T", "cs:Z:=ACT+ccc=T"]
cigar_list = ["4M", "4M", "1S3M", "3M", "3M3I1M"]
pos_list = [1, 1, 1, 2, 1]
cstag.consensus(cs_list, cigar_list, pos)
# => cs:Z:=AC*gt*T
```