[![Licence](https://img.shields.io/badge/License-MIT-9cf.svg)](https://choosealicense.com/licenses/mit/)
[![Test](https://img.shields.io/github/actions/workflow/status/akikuno/cstag/pytest.yml?branch=main&label=Test&color=brightgreen)](https://github.com/akikuno/cstag/actions)
[![Python](https://img.shields.io/pypi/pyversions/cstag.svg?label=Python&color=blue)](https://pypi.org/project/cstag/)
[![PyPI](https://img.shields.io/pypi/v/cstag.svg?label=PyPI&color=orange)](https://pypi.org/project/cstag/)
[![Bioconda](https://img.shields.io/conda/v/bioconda/cstag?label=Bioconda&color=orange)](https://anaconda.org/bioconda/cstag)
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
- `cstag.revcomp()`: Converts a CS tag into its reverse complement
- `cstag.to_sequence()`: Output a reference subsequence in the alignment
- `cstag.to_vcf()`: Output a VCF
- `cstag.to_html()`: Output a HTML

Visit the [documentation](https://akikuno.github.io/cstag/cstag/) for more details.  
For adding CS tags to SAM/BAM files, [`cstag-cli`](https://github.com/akikuno/cstag-cli) is at your service.  

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

print(cstag.call(cigar, md, seq))
# :2*ag:5-ag:4+ac~nn3nn:1

cstag.call(cigar, md, seq, long=True)
# =AC*ag=TACGT-ag=ACGT+ac~nn3nn=G
```

### Shorten or Lengthen CS Tags

```python
import cstag

# Convert a CS tag from long to short
cs_tag = "=ACGT*ag=CGT"

cstag.shorten(cs_tag)
# :4*ag:3


# Convert a CS tag from short to long
cs_tag = ":4*ag:3"
cigar = "8M"
seq = "ACGTACGT"

cstag.lengthen(cs_tag, cigar, seq)
# =ACGT*ag=CGT
```

### Generate a Consensus

```python
import cstag

cs_tags = ["=ACGT", "=AC*gt=T", "=C*gt=T", "=C*gt=T", "=ACT+ccc=T"]
positions = [1, 1, 2, 2, 1]

cstag.consensus(cs_tags, positions)
# =AC*gt*T
```

### Mask Low-Quality Bases

```python
import cstag

cs_tag = "=ACGT*ac+gg-cc=T"
cigar = "5M2I2D1M"
qual = "AA!!!!AA"
phred_threshold = 10
cstag.mask(cs_tag, cigar, qual, phred_threshold)
# =ACNN*an+ng-cc=T
```

### Split a CS Tag

```python
import cstag

cs_tag = "=ACGT*ac+gg-cc=T"
cstag.split(cs_tag)
# ['=ACGT', '*ac', '+gg', '-cc', '=T']
```

### Reverse Complement of a CS Tag

```python
import cstag

cs_tag = "=ACGT*ac+gg-cc=T"
cstag.revcomp(cs_tag)
# =A-gg+cc*tg=ACGT
```

### Reconstruct the reference subsequence in the alignment

```python
import cstag
cs_tag = "=AC*gt=T-gg=C+tt=A"
cstag.to_sequence(cs_tag)
# ACTTCTTA
```

### Generate VCF Report

```python
import cstag
cs_tag = "=AC*gt=T-gg=C+tt=A"
chrom = "chr1"
pos = 1
print(cstag.to_vcf(cstag, chrom, pos))
"""
##fileformat=VCFv4.2
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
chr1	3	.	G	T	.	.	.
chr1	4	.	TGG	T	.	.	.
chr1	5	.	C	CTT	.	.	.
"""
```

### Generate HTML Report

```python
import cstag
from pathlib import Path

cs_tag = "=AC+ggg=T-acgt*at~gt10ag=GNNN"
description = "Example"

cs_tag_html = cstag.to_html(cs_tag, description)
Path("report.html").write_text(cs_tag_html)
# Output "report.html"
```
The resulting `report.html` looks like this :point_down:

<img width="511" alt="image" src="https://user-images.githubusercontent.com/15861316/265405607-a3cc1b76-f6a2-441d-b282-6f2dc06fc03d.png">

## 📣Feedback

For questions, bug reports, or any other inquiries, feel free to reach out!  
Please use [GitHub Issues](https://github.com/akikuno/cstag/issues) for reporting.
