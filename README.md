[![Licence](https://img.shields.io/badge/License-MIT-9cf.svg?style=flat-square)](https://choosealicense.com/licenses/mit/)
[![Test](https://img.shields.io/github/actions/workflow/status/akikuno/cstag/pytest.yml?branch=main&label=Test&color=brightgreen&style=flat-square)](https://github.com/akikuno/cstag/actions)
[![Python](https://img.shields.io/pypi/pyversions/cstag.svg?label=Python&color=blue&style=flat-square)](https://pypi.org/project/cstag/)
[![PyPI](https://img.shields.io/pypi/v/cstag.svg?label=PyPI&color=orange&style=flat-square)](https://pypi.org/project/cstag/)
[![Bioconda](https://img.shields.io/conda/v/bioconda/cstag?label=Bioconda&color=orange&style=flat-square)](https://anaconda.org/bioconda/cstag)
[![DOI](https://zenodo.org/badge/468937655.svg)](https://zenodo.org/badge/latestdoi/468937655)

# cstag

`cstag` is a Python library designed for handling and manipulating [minimap2's CS tags](https://github.com/lh3/minimap2#cs).

## 🌟Features

- `cstag.call()`: Generate a CS tag
- `cstag.shorten()`: Convert a CS tag from long to short format
- `cstag.lengthen()`: Convert a CS tag from short to long format
- `cstag.consensus()`: Generate a consensus cs tag from multiple cs tags
- `cstag.mask()`: Mask low-quality bases in a CS tag
- `cstag.split()`: Split a CS tag
- `cstag.revcomp()`: Converts a CS tag into its reverse complement.
- `cstag.to_html()`: Output html report

Visit the [documentation](https://akikuno.github.io/cstag/cstag/) for more details.

## 🛠 Installation

Using [PyPI](https://pypi.org/project/cstag/):

```bash
pip install cstag
```

Using [Bioconda](https://anaconda.org/bioconda/cstag):

```bash
conda install -c bioconda cstag
```

## 💡Usage

### Generate CS Tags
```python
import cstag

cigar = "8M2D4M2I3N1M"
md = "2A5^AG7"
seq = "ACGTACGTACGTACG"

cstag.call(cigar, md, seq)
# => :2*ag:5-ag:4+ac~nn3nn:1

cstag.call(cigar, md, seq, is_long=True)
# => =AC*ag=TACGT-ag=ACGT+ac~nn3nn=G
```

### Shorten or Lengthen CS Tags

```python
import cstag

# Convert a CS tag from long to short
cs = "=ACGT*ag=CGT"

cstag.shorten(cs)
# => :4*ag:3


# Convert a CS tag from short to long
cs = ":4*ag:3"
cigar = "8M"
seq = "ACGTACGT"

cstag.lengthen(cs, cigar, seq)
# => =ACGT*ag=CGT
```

### Generate a Consensus

```python
import cstag

cs_list = ["=ACGT", "=AC*gt=T", "=C*gt=T", "=C*gt=T", "=ACT+ccc=T"]
cigar_list = ["4M", "4M", "1S3M", "3M", "3M3I1M"]
pos_list = [1, 1, 1, 2, 1]

cstag.consensus(cs_list, cigar_list, pos_list)
# => =AC*gt*T
```

### Mask Low-Quality Bases

```python
import cstag

cs = "=ACGT*ac+gg-cc=T"
cigar = "5M2I2D1M"
qual = "AA!!!!AA"
phred_threshold = 10
cstag.mask(cs, cigar, qual, phred_threshold)
# => =ACNN*an+ng-cc=T
```

### Split a CS Tag

```python
import cstag

cs = "=ACGT*ac+gg-cc=T"
cstag.split(cs)
# => ['', '=ACGT', '*ac', '+gg', '-cc', '=T']
```

### Reverse Complement of a CS Tag

```python
import cstag

cs = "=ACGT*ac+gg-cc=T"
cstag.revcomp(cs)
# => =A-gg+cc*tg=ACGT
```


### Generate HTML Report

```python
import cstag
from pathlib import Path

cs = "=AC+GGG=T-ACGT*at~gt10cg=GNNN"
description = "Example"

cstag_html = cstag.to_html(cs, description)
Path("report.html").write_text(cstag_html)
# => Output "report.html"
```
The resulting `report.html` looks like this :point_down:

<img width="414" alt="example_report" src="https://user-images.githubusercontent.com/15861316/158910398-67f480d2-8742-412a-b528-40e545c46513.png">

## 📣Feedback

For questions, bug reports, or any other inquiries, feel free to reach out!  
Please use [GitHub Issues](https://github.com/akikuno/cstag/issues) for reporting.
