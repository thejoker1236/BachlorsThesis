# Bachelor's Thesis

**Wie funktionieren KI-gestützte Monitoring-Systeme als digitale Informationssysteme und inwiefern ermöglichen sie datenbasierte Analyse und Beeinflussung von Verhalten?**

Meshan Fernando — FOM Hochschule, Studienzentrum Frankfurt

## Prerequisites

### 1. Install TeX Live

Download and install [TeX Live](https://www.tug.org/texlive/) (2026 or later).

During installation, select the full scheme or at minimum include the following collections.

### 2. Install Required LaTeX Packages

Open PowerShell **as Administrator** and run:

```powershell
C:\texlive\2026\bin\windows\tlmgr.bat install collection-latexextra collection-fontsrecommended babel-german hyphen-german
```

This installs all packages needed to compile the thesis.

## Getting Started

Compile the thesis PDF from the repo root:

```powershell
.\scripts\compile.ps1
```

The script will compile `Paper/main.tex` (running pdflatex + biber three times for correct references) and open the resulting `Paper/main.pdf` in Microsoft Edge.
