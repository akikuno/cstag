[![Licence](https://img.shields.io/badge/License-MIT-blue.svg)](https://choosealicense.com/licenses/mit/)
[![Test](https://github.com/akikuno/cstag/actions/workflows/test.yml/badge.svg)](https://github.com/akikuno/cstag/actions/workflows/test.yml?query=workflow%3APytest)
<!-- [![PyPI](https://img.shields.io/badge/Install%20with-PyPI-brightgreen.svg)](https://pypi.org/project/cstag/) -->
<!-- [![Bioconda](https://img.shields.io/badge/Install%20with-Bioconda-brightgreen.svg)](https://anaconda.org/bioconda/cstag) -->

# cstag

`cstag` is a Python module to convert a [minimap2's CS tag](https://github.com/lh3/minimap2#cs) from short to long format, vice versa.

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
# Convert short format of cs tag into long format
import cstag
cs = "cs:Z::4*ag:3"
cigar = "8M"
seq = "ACGTACGT"
cstag.lengthen(cs, cigar, seq)
# cs:Z:=ACGT*ag=CGT
```

## Documentation

https://akikuno.github.io/cstag/cstag/cstag.html