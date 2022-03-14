[![Licence](https://img.shields.io/badge/License-MIT-blue.svg)](https://choosealicense.com/licenses/mit/)
[![Test](https://github.com/akikuno/cstag/actions/workflows/test.yml/badge.svg)](https://github.com/akikuno/cstag/actions/workflows/test.yml?query=workflow%3APytest)
<!-- [![PyPI](https://img.shields.io/badge/Install%20with-PyPI-brightgreen.svg)](https://pypi.org/project/calcs/) -->
<!-- [![Bioconda](https://img.shields.io/badge/Install%20with-Bioconda-brightgreen.svg)](https://anaconda.org/bioconda/calcs) -->


# cstag

`cstag` is a Python module to convert a [minimap2's CS tag](https://github.com/lh3/minimap2#cs) from short to long format, vice versa.

## Install

You can install `cstag` using pip or conda:

```bash
pip install cstag
```

```bash
conda install -c bioconda cstag
```

## Usage

```python
import cstag
cstag.shorten()
cstag.lengthen()
```