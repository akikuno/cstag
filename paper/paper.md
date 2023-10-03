---
title: 'cstag: A Python Package for manipulating and visualizing CS tags'
tags:
  - python
  - genomics
  - sequencing
  - bioinformatics
authors:
  - name: Akihiro Kuno
    orcid: 0000-0002-4674-6882
    corresponding: true
   affiliation: "1"
affiliations:
 - name: Department of Anatomy and Embryology, University of Tsukuba, Tsukuba, Ibaraki, Japan
   index: 1
date: 30 October 2023
bibliography: paper.bib
---

<!-- ---
title: cstag: A Python Package for manipulating and visualizing CS tags
tags:
  - python
  - genomics
  - sequencing
  - bioinformatics
authors:
  - name: Akihiro Kuno
    orcid: 0000-0002-4674-6882
    corresponding: true
    affiliation: 1
affiliations:
 - name: Department of Anatomy and Embryology, University of Tsukuba, Tsukuba, Ibaraki, Japan
   index: 1
date: 30 October 2023
bibliography: paper/paper.bib
--- -->

# Summary
With the widespread commoditization of DNA sequencers, the scientific community is generating an unprecedented volume of sequence alignments on a daily basis. Conventionally, the task of identifying specific mutations or reconstructing reference subsequences from alignment data has been cumbersome and resource-intensive. This often involved intricate processes requiring the cross-referencing of multiple elements like query sequences, CIGAR strings, and MD tags. However, in recent years, a new tag called the CS tag has been developed [@minimap2], which encapsulates the information contained in both CIGAR strings and MD tags. The CS tags enable researchers to represent mutations within alignments in a far more intuitive and streamlined manner.

This paper introduces two tools aimed at harnessing CS tags: a Python library named `cstag` for the efficient manipulation and visualization of CS tags, and a command-line utility called `cstag-cli` that facilitates the addition of CS tags to SAM/BAM files. These tools are designed to utilize the representational capabilities of CS tags, thereby streamlining the process of extracting essential mutation information from sequence alignments.


# Statement of Need

The CS tag serves as a relatively novel format for encoding information pertinent to sequence alignment[@minimap2]. Compared to traditional formats such as CIGAR and MD tags, the CS tag offers the unique capability to encode multiple types of sequence variations—namely mismatches, insertions, deletions, and splice sites—within a single tag. In contrast, extracting comprehensive variant information from CIGAR and MD tags necessitates intricate cross-referencing and interpretation between them, which can be computationally challenging. Additionally, the CS tag in long form encapsulates which bases in the query sequence map directly to specific bases in the reference sequence, thereby enhancing interpretability. As a result of this consolidated approach to encoding sequence alignment information, the CS tag simplifies tasks that traditionally required the mutual referencing of CIGAR, MD tags, and query sequences. This advantage has led to the incorporation of the CS tag in several bioinformatics tools, effectively streamlining the process of variant identification and analysis[@DAJIN; @2passtools].

The cstag and cstag-cli to further use the expression of the CS tag. The cstag is a Python toolkit for performing various operations and visualizations on CS tags, while cstag-cli is a command-line tool for adding CS tags to existing SAM/BAM files.

The cstag performs to split and process sequence variation information, generate its reverse complement, and create consensus sequences. Additionally, cstag can convert the variation information represented by the CS tag (mismatches, insertions, deletions, splice sites, unknown) into Variant Call Format (VCF) files, or output it as HTML or PDF. Converting to VCF allows for visualization in genome browsers like IGV[@igv], and using HTML/PDF enables the creation of publication-ready figures (Figure 1). As an actual use case, the authors have clarified the variation information in samples by obtaining a consensus of multiple CS tags generated through Target sequencing and subsequently visualizing them[@DAJIN].

<!-- ![Visualization of CS tags by VCF and HTML outputs.](cstag_visualization.png) -->

Furthermore, cstag-cli was developed as a command-line tool for adding CS tags. While paftools [@minimap2] calls the CS tags from SAM/BAM files, it changes the file format to PAF. Although the PAF is a lightweight and convenient format, SAM/BAM format is more  commonly used as input for various tools. Therefore, cstag-cli was created to add CS tags without changing the file format. cstag-cli is a command-line tool that takes SAM/BAM files as input and outputs SAM with CS tags to standard output. Since SAM/BAM can be received from standard input, it is easy to integrate cstag-cli into existing scripts. This allows the user to obtain CS tags without altering the format of the existing SAM/BAM files.

# Availability
cstag and cstag-cli are distributed on PyPI under the MIT License. Conda packages are also available in the Bioconda channel [@bioconda]. The source code is available in a git repository on GitHub at https://github.com/akikuno/cstag and https://github.com/akikuno/cstag-cli, and features a Continuous Integration workflow to run integration tests on changes. Documentation of cstag is hosted on [pdoc3](https://akikuno.github.io/cstag/cstag/) and built for each new release.

# Acknowledgements

I would like to extend my gratitude to Dr. Satoru Takahashi from the Department of Anatomy and Embryology at the University of Tsukuba for his invaluable discussions. I also acknowledge the support received from the Laboratory Animal Resource Center at the University of Tsukuba.

# References



