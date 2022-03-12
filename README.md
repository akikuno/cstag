# cstag

`cstag` is a Python module to convert a [cs tag](https://lh3.github.io/minimap2/minimap2.html#:~:text=harboring%20repetitive%20seeds-,The%20cs%20tag,-encodes%20difference%20sequences) from short to long format, vice versa.

## Install

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
