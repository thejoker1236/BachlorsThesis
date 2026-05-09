# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Bachelor's thesis project focused on machine learning applied to computer systems and networking. The research direction involves unsupervised machine learning techniques for network analysis (see reference materials in `Expose/Quellen/` and the PDFs at the project root).

The project is in the writing phase. The thesis paper is being authored in LaTeX.

## Repository Structure

```
Expose/               # Thesis proposal (Exposé) in .docx and .pdf
Expose/Quellen/       # Reference papers and source notes
HowTo/                # Formal thesis guidelines and example presentations from the university
Paper/                # Thesis paper in LaTeX format
  main.tex            # Main LaTeX source file
  references.bib      # Bibliography
  main.pdf            # Compiled output
  compile.ps1         # PowerShell script to compile the LaTeX document
*.pdf                 # Background reading: ML for networking, TCP/IP, unsupervised ML
```

## Compiling the Paper

Run the compile script from the `Paper/` directory:

```powershell
cd Paper
./compile.ps1
```

## When Implementation Begins

Update this file with:
- Language/framework chosen and how to install dependencies
- How to run the project and any experiments
- How to run tests
- Description of the module/component architecture
