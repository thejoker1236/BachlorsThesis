---
name: latex-thesis-compilation
description: Guidance for automating LaTeX thesis compilation workflows at FOM Hochschule. Use when creating or modifying compilation scripts, debugging LaTeX errors, validating against FOM guidelines, or managing auxiliary files and incremental builds.
---

# LaTeX Thesis Compilation Skill

## Purpose
This skill provides guidance for automating LaTeX thesis compilation workflows at FOM Hochschule, including multi-pass compilation, bibliography processing with biber, and FOM guideline validation.

## Context
Use this skill when:
- Creating or modifying LaTeX compilation scripts
- Debugging LaTeX compilation errors
- Validating thesis documents against FOM guidelines
- Managing auxiliary files and output PDFs
- Implementing incremental build detection

## Key Concepts

### Compilation Workflow
LaTeX documents require multiple compilation passes to resolve cross-references:
1. **Pass 1**: Initial compilation generates `.aux` file with reference data
2. **Biber**: Processes bibliography from `references.bib` → generates `.bbl` file
3. **Pass 2**: Integrates bibliography references
4. **Pass 3**: Finalizes cross-references and table of contents

### FOM Hochschule Guidelines
- **Margins**: Left 4cm, Right 2cm, Top 2.5cm, Bottom 2cm
- **Font**: Times New Roman 12pt with 1.5 line spacing
- **Required Front Matter**: Titelblatt, Inhaltsverzeichnis, Abbildungsverzeichnis, Abkürzungsverzeichnis, Formelverzeichnis, Tabellenverzeichnis
- **Required Back Matter**: Literaturverzeichnis, Ehrenwörtliche Erklärung

### Auxiliary Files
Temporary files generated during compilation that should be preserved for incremental builds:
`.aux`, `.bbl`, `.bcf`, `.blg`, `.log`, `.out`, `.toc`, `.lof`, `.lot`, `.run.xml`, `.equ`, `.fls`, `.fdb_latexmk`, `.synctex.gz`

## Required Tools
- **pdflatex**: LaTeX compiler (TeX Live 2026+)
- **biber**: Bibliography processor
- **Required Packages**: collection-latexextra, collection-fontsrecommended, babel-german, hyphen-german, biblatex

## Implementation Patterns

### PowerShell Compilation Script Structure
```powershell
# 1. Validate environment
Test-LaTeXEnvironment -RequiredExecutables @('pdflatex', 'biber')

# 2. Parse document structure
$structure = Get-DocumentStructure -MainDocument "Paper/main.tex"

# 3. Execute compilation passes
Push-Location Paper
try {
    # Pass 1
    pdflatex -interaction=nonstopmode -file-line-error main.tex
    
    # Bibliography processing
    biber main
    
    # Pass 2 & 3
    pdflatex -interaction=nonstopmode -file-line-error main.tex
    pdflatex -interaction=nonstopmode -file-line-error main.tex
}
finally {
    Pop-Location
}

# 4. Copy output
Copy-Item "Paper/main.pdf" "Bachelor-Thesis_Fernando_KI-Monitoring-Systeme.pdf"
```

### Error Detection and Reporting
```powershell
# Parse .log file for errors
$errors = Select-String -Path "Paper/main.log" -Pattern "^!" 
foreach ($error in $errors) {
    # Extract file, line, message
    Write-Error "LaTeX Error: $($error.Line)"
}

# Parse .blg file for bibliography errors
$bibErrors = Select-String -Path "Paper/main.blg" -Pattern "ERROR|WARN"
```

### Incremental Build Detection
```powershell
# Check if compilation is needed
$sourcesModified = (Get-ChildItem Paper/*.tex -Recurse).LastWriteTime | Measure-Object -Maximum
$pdfModified = (Get-Item "Bachelor-Thesis_*.pdf").LastWriteTime

if ($sourcesModified.Maximum -le $pdfModified) {
    Write-Host "PDF is up-to-date"
    return
}
```

### FOM Guideline Validation
```powershell
# Check geometry package settings
$geometryLine = Select-String -Path "Paper/main.tex" -Pattern "\\usepackage\[.*\]{geometry}"
if ($geometryLine -match "left=4cm.*right=2cm.*top=2.5cm.*bottom=2cm") {
    Write-Host "✓ Margins comply with FOM guidelines"
}

# Check required sections
$requiredSections = @('Titelblatt', 'Inhaltsverzeichnis', 'Literaturverzeichnis')
foreach ($section in $requiredSections) {
    if (-not (Select-String -Path "Paper/main.tex" -Pattern $section -Quiet)) {
        Write-Warning "Missing required section: $section"
    }
}
```

## Common Error Scenarios

### Missing Package Errors
**Pattern**: `! LaTeX Error: File 'package.sty' not found.`

**Solution**:
```powershell
tlmgr install package-name
```

### Undefined Reference Warnings
**Pattern**: `LaTeX Warning: Reference 'label' on page X undefined.`

**Cause**: Need additional compilation pass or missing `\label{}` commands

**Solution**: Run additional pdflatex pass or add missing labels

### Bibliography Errors
**Pattern**: `WARN - I didn't find a database entry for "citekey"`

**Cause**: Citation key in `.tex` doesn't exist in `references.bib`

**Solution**: Fix citation key or add entry to bibliography file

### File Path Errors on Windows
**Issue**: Paths with spaces or special characters fail

**Solution**: Quote paths in shell commands:
```powershell
& pdflatex -interaction=nonstopmode "`"$MainDocument`""
```

## Testing Approaches

### Unit Tests (Pester)
```powershell
Describe "Environment Validation" {
    It "Detects pdflatex in PATH" {
        Get-Command pdflatex -ErrorAction SilentlyContinue | Should -Not -BeNullOrEmpty
    }
}

Describe "Document Parsing" {
    It "Extracts chapter files from main.tex" {
        $structure = Get-DocumentStructure -MainDocument "main.tex"
        $structure.ChapterFiles | Should -Contain "chapters/01_einleitung.tex"
    }
}
```

### Integration Tests
```powershell
Describe "Full Compilation" {
    It "Produces PDF with correct filename" {
        & .\scripts\compile.ps1
        "Bachelor-Thesis_Fernando_KI-Monitoring-Systeme.pdf" | Should -Exist
    }
}
```

## Best Practices

1. **Always use `-interaction=nonstopmode`** to prevent interactive prompts
2. **Preserve working directory context** with `Push-Location`/`Pop-Location`
3. **Parse log files on error** to provide actionable diagnostics
4. **Validate environment first** before attempting compilation
5. **Use platform-appropriate path handling** for cross-platform compatibility
6. **Implement retry logic** for file copy operations (handle locked files)
7. **Report progress at each stage** for long-running compilations
8. **Clean auxiliary files** only when explicitly requested (preserve for incremental builds)

## File Structure Reference
```
BachlorsThesis/
├── Paper/
│   ├── main.tex              # Main document
│   ├── references.bib        # Bibliography database
│   ├── chapters/             # Chapter files
│   │   ├── 01_einleitung.tex
│   │   ├── 02_grundlagen.tex
│   │   └── ...
│   └── pic/                  # Images
├── scripts/
│   └── compile.ps1           # Compilation script
├── HowTo/                    # FOM guidelines
└── Bachelor-Thesis_*.pdf     # Output (root)
```

## References
- TeX Live Documentation: https://www.tug.org/texlive/
- Biber/BibLaTeX Manual: https://ctan.org/pkg/biblatex
- FOM Guidelines: Located in `HowTo/` directory
- PowerShell Best Practices: https://docs.microsoft.com/powershell/

## When to Use This Skill
Activate this skill when:
- User asks about LaTeX compilation
- User mentions thesis, PDF generation, or bibliography
- User works with `.tex`, `.bib`, or LaTeX-related files
- User mentions pdflatex, biber, or TeX Live
- User asks about FOM guidelines or thesis formatting
