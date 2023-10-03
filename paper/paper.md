---
title: '`cstag` and `cstag-cli`: tools for manipulating and visualizing CS tags'
tags:
  - python
  - genomics
  - sequencing
  - bioinformatics
authors:
  - name: Akihiro Kuno
    orcid: 0000-0002-4674-6882
    corresponding: true
    affiliation: "1, 2"
affiliations:
  - name: Department of Anatomy and Embryology, University of Tsukuba, Tsukuba, Ibaraki, Japan
    index: 1
  - name: Laboratory Animal Resource Center, Trans-border Medical Research Center, University of Tsukuba, Tsukuba, Ibaraki, Japan.
    index: 2
date: 30 October 2023
bibliography: paper.bib
---

# Summary

With the widespread commoditization of DNA sequencers, the scientific community is generating an unprecedented volume of sequence alignments on a daily basis. Conventionally, the task of identifying specific mutations or reconstructing reference subsequences from alignment data has been cumbersome and resource-intensive. This often involved intricate processes requiring the cross-referencing of multiple elements like query sequences, CIGAR strings, and MD tags. However, in recent years, a new tag called the CS tag has been developed [@Heng2018], which encapsulates the information contained in both CIGAR strings and MD tags. The CS tags enable researchers to represent mutations within alignments in a far more intuitive and streamlined manner.

This paper presents two tools optimized for the use of CS tags: the `cstag`, a Python library designed for effective manipulation and visualization of CS tags, and `cstag-cli`, a command-line utility for seamlessly appending CS tags to SAM/BAM files. By leveraging the representational strengths of CS tags, these tools simplify the extraction of critical mutation data from sequence alignments.

# Statement of Need

The CS tag introduces a relatively new format for encoding information related to sequence alignment[@Heng2018]. While traditional formats, like CIGAR and MD tags, play crucial roles, the CS tag stands out by encoding a variety of sequence variations—including mismatches, insertions, deletions, and splice sites—all within one unified tag. To extract comprehensive variant data from CIGAR and MD tags, users often face the complexity of cross-referencing and interpreting between these tags, a task that can be intensive. On the other hand, the long form of the CS tag clearly indicates which bases from the query sequence align to specific bases in the reference sequence, improving its interpretability. As a result, the CS tag has simplified tasks that previously relied on mutual referencing between CIGAR, MD tags, and query sequences. This efficiency has led to the widespread adoption of the CS tag in various bioinformatics tools, enhancing the process of variant identification and analysis [@Kuno2022; @Parker2021].

Here, the author has developed `cstag` and `cstag-cli` to further use the expression of the CS tag. `cstag` is a Python toolkit designed for a range of operations and visualizations related to CS tags. In contrast, `cstag-cli` serves as a command-line utility focused on appending CS tags to pre-existing SAM/BAM files. `cstag` performs to split and process sequence variation information, generate its reverse complement, and create consensus sequences. Additionally, `cstag` can convert the variation information represented by the CS tag into Variant Call Format (VCF) files. In addition, it can produce outputs in HTML/PDF formats. The VCF conversion facillitates visualization in genome browsers, such as IGV [@Robinson2011], while the HTML/PDF formats cater to the generation of publication-ready visuals. To illustrate its practical application, the authors have demonstrated how variation information in samples can be elucidated by deriving a consensus from multiple CS tags produced via Nanopore target sequencing, and subsequently visualizing the results [@Kuno2022].
<!-- ![Visualization of CS tags by VCF and HTML outputs.](cstag_visualization.png) -->

Additionally, `cstag-cli` has been developed as a command-line tool specifically for appending CS tags to SAM/BAM files. While paftools [@Heng2018] can extract CS tags from these files, it converts them to the PAF format. Even though PAF is a lightweight and user-friendly format, the SAM/BAM format remains the predominant choice for many bioinformatics tools. Recognizing this preference, `cstag-cli` was designed to add CS tags directly to the original files without necessitating any format change. Accepting SAM/BAM files as input, `cstag-cli` outputs them with appended CS tags to the standard output. Given the tool's ability to directly process SAM/BAM files from standard input, it seamlessly integrates into existing scripts, enabling users to access CS tags without modifying their existing SAM/BAM file structures.


# Availability

`cstag` and `cstag-cli` are distributed on PyPI under the MIT License. Conda packages are also available in the Bioconda channel [@Grüning2018]. The source code is available in a git repository on GitHub at https://github.com/akikuno/cstag and https://github.com/akikuno/cstag-cli, and features a Continuous Integration workflow to run integration tests on changes. Documentation of `cstag` is hosted on [pdoc3](https://akikuno.github.io/cstag/cstag/) and built for each new release.

# Acknowledgements

I would like to extend my gratitude to Dr. Satoru Takahashi from the Department of Anatomy and Embryology at the University of Tsukuba for his invaluable discussions. I also acknowledge the support received from the Laboratory Animal Resource Center at the University of Tsukuba.

# References



