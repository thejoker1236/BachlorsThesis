---
name: latex-thesis-workflow
description: Comprehensive workflow for LaTeX thesis operations with MANDATORY compilation and error-fixing. Includes chapter updates, citation management, automatic error detection/fixing loop, and git workflow. Always compiles after edits and fixes errors iteratively until successful.
---

# LaTeX Thesis Workflow - Comprehensive Guide

## Purpose
This consolidated skill provides complete guidance for all LaTeX thesis operations:
- **Chapter Updates**: Replacing/updating thesis sections with proper formatting
- **Citation Management**: Converting inline citations to footnote format and managing bibliography
- **Compilation with Error Fixing**: Multi-pass LaTeX compilation with automatic error detection and fixing loop
- **Git Workflow**: Staging, committing changes with auto-generated PDFs

**CRITICAL: This workflow now includes MANDATORY compilation and error-fixing (Phase 6). You must compile after finishing edits and fix any errors iteratively until compilation succeeds.**

## When to Use
- User provides text content to replace/update a thesis section
- User provides text with inline citations needing conversion
- User asks to update section numbers (e.g., "2.2.3", "3.1.2")
- User asks about compilation, PDF generation, or bibliography
- User asks to commit changes or stage PDFs
- Any thesis content modification (compilation is always mandatory afterward)

## Complete Workflow for Chapter Updates with Citations

### Phase 1: Identify Target Section (NO HOOK TO DISABLE ANYMORE)
When user provides content like:
```
2.2.3 Plattformökosysteme
Die moderne Informationsökonomie...
```

Extract:
- **Chapter number**: `2` → `02_grundlagen.tex`
- **Section level**: `2.2.3` → subsection (three levels deep)
- **Section title**: `Plattformökosysteme`

**Chapter File Mapping:**
- `01_einleitung.tex` - Introduction
- `02_grundlagen.tex` - Theoretical foundations
- `03_monitoring_systeme.tex` - Monitoring systems
- `04_implikationen.tex` - Implications
- `05_kritische_betrachtung.tex` - Critical analysis
- `06_fazit.tex` - Conclusion

### Phase 2: Citation Analysis and Conversion

#### Step 2.1: Identify All Citations
Parse the user's text for citation patterns:
- `(vgl. Author 2016, S. 123)`
- `(vgl. Author, Author2 und Author3 2020, S. 45)`
- `(vgl. Author 2018)`
- `¹ Vgl. Author (2016), S. 30.` (footnote format)

#### Step 2.2: Read Bibliography and Match Citations
1. Read `Paper/references.bib`
2. Extract all BibTeX keys (e.g., `Tiwana2014`, `Parker2016`, `Srnicek2017`)
3. Match each citation to existing keys

**Matching Examples:**
```
Tiwana (2014), S. 5 → Tiwana2014
Parker, Van Alstyne und Choudary (2016), S. 17 → Parker2016
Cusumano, Gawer und Yoffie (2019), S. 18 → Cusumano2019
Srnicek (2017), S. 29 → Srnicek2017
```

#### Step 2.3: Handle Missing Sources
If citation NOT found in references.bib:
1. Create list of missing sources
2. Ask user for complete bibliographic information:
   - **Books**: Authors, Title, Year, Edition, Publisher, Location
   - **Articles**: Authors, Title, Journal, Year, Volume, Number, Pages, DOI

#### Step 2.4: Generate BibTeX Keys for New Sources
Follow existing convention:
- Single author: `LastName+Year` (e.g., `Pasquale2015`)
- Two authors: `LastName1LastName2+Year` (e.g., `RussellNorvig2010`)
- Three+ authors: `FirstAuthorLastName+Year` (e.g., `Laudon2016`)

#### Step 2.5: Add Missing Entries to references.bib
1. Determine appropriate section (e.g., `% Kapitel 2 — ...`)
2. Format entry according to existing style
3. Insert in alphabetical order within section

**Example Entry:**
```bibtex
@book{Tiwana2014,
  author    = {Tiwana, Amrit},
  title     = {Platform Ecosystems: Aligning Architecture, Governance, and Strategy},
  year      = {2014},
  publisher = {Morgan Kaufmann},
  address   = {Waltham, MA}
}
```

#### Step 2.6: Convert All Citations to \vglfootcite Format
**Conversion Pattern:**
```
(vgl. Author(s) Year, S. Page) → \vglfootcite[Page]{BibTeXKey}
```

**Conversion Examples:**
```
¹ Vgl. Tiwana (2014), S. 5.
→ \vglfootcite[5]{Tiwana2014}

² Vgl. Parker, Van Alstyne und Choudary (2016), S. 17.
→ \vglfootcite[17]{Parker2016}

³ Vgl. Srnicek (2017), S. 29–30.
→ \vglfootcite[29--30]{Srnicek2017}

⁴ Vgl. Author (2020), S. 12 f.
→ \vglfootcite[12\,f.]{Author2020}

⁵ Vgl. Author (2018).
→ \vglfootcite{Author2018}
```

**Special Page Notation (Preserve!):**
- `S. 12\,f.` = page 12 and following
- `S. 12\,ff.` = page 12 and several following
- `S. 29--30` = pages 29 to 30

### Phase 3: Format and Replace Section Content

#### Step 3.1: Format LaTeX Content
Convert user's text to proper LaTeX:
- Add proper section header: `\subsection{Title}`
- Preserve paragraph breaks (double newlines)
- Convert citations to `\vglfootcite` commands
- Place citations AFTER punctuation: `text.\vglfootcite[10]{Key}`
- Use `--` for en-dash (e.g., "den Plattformbetreiber, die Komplementoren sowie die Nutzer --")
- Escape special chars: `\ac{KI}` for acronyms

#### Step 3.2: Read Existing Section
Read the target chapter file to find existing content:
```powershell
grep -n "\\subsection{.*}" Paper/chapters/02_grundlagen.tex
```

#### Step 3.3: Replace Section
Use `str_replace` with:
- **oldStr**: Complete original section (header + all content until next section)
- **newStr**: New formatted section with proper citations
- **Include enough context** to ensure unique match (e.g., surrounding paragraph)

**Handle Duplicates:** If title appears multiple times, include parent section context.

### Phase 4: Pre-Compilation Validation (OPTIONAL BUT RECOMMENDED)

#### Step 4.1: Verify All Citations
Cross-check all `\vglfootcite` commands:
1. Extract all BibTeX keys used
2. Verify each exists in `references.bib`
3. Report any missing keys

#### Step 4.2: Check for Duplicate Citations
Ensure no citation appears twice in same sentence:
```
❌ WRONG: Text.\vglfootcite[30]{Key} More (vgl. Author 2016, S. 30).
✓ CORRECT: Text.\vglfootcite[30]{Key} More text.
```

### Phase 6: Compile and Fix Errors (MANDATORY)

**CRITICAL: After completing all edits, you MUST compile the thesis and fix any errors until compilation succeeds.**

#### Step 6.1: Run Initial Compilation
Execute the compilation script:
```powershell
.\scripts\compile.ps1
```

**Compilation Process (Multi-Pass):**
1. **Pass 1**: `pdflatex main.tex` (generates `.aux`)
2. **Biber**: `biber main` (processes bibliography)
3. **Pass 2**: `pdflatex main.tex` (integrates references)
4. **Pass 3**: `pdflatex main.tex` (finalizes cross-refs)
5. **Copy**: `main.pdf` → `Bachelor-Thesis_Fernando_KI-Monitoring-Systeme.pdf`

#### Step 6.2: Check Compilation Result

**If Compilation Succeeds (Exit Code 0):**
- ✓ All citations resolved (no "undefined reference" warnings)
- ✓ Bibliography generated correctly
- ✓ PDF created successfully
- ✓ Complies with FOM guidelines
- → **Proceed to Phase 7 (Git Workflow)**

**If Compilation Fails (Exit Code ≠ 0):**
- → **Execute Error Fix Loop (Step 6.3)**

#### Step 6.3: Error Fix Loop (MANDATORY UNTIL SUCCESS)

**DO NOT PROCEED until compilation succeeds. Follow this loop:**

1. **Analyze Error Output:**
   - Read the compilation script output
   - Identify the specific error type:
     - LaTeX syntax errors (missing braces, invalid commands)
     - Undefined citations (citation key not in references.bib)
     - Bibliography errors (biber warnings/errors)
     - Missing packages or fonts
     - File not found errors
     - Cross-reference errors

2. **Fix the Error:**
   
   **For Undefined Citation Errors:**
   ```
   Pattern: "Citation 'KeyName' undefined"
   ```
   - Check if BibTeX key exists in `Paper/references.bib`
   - If missing: Ask user for source details and add entry
   - If typo: Fix the citation key in the .tex file
   - Verify key spelling matches exactly

   **For LaTeX Syntax Errors:**
   ```
   Pattern: "! LaTeX Error: ..." or "! Undefined control sequence"
   ```
   - Read the error line number from output
   - Open the file and go to that line
   - Fix the syntax issue:
     - Add missing closing braces `}`
     - Escape special characters (`&`, `%`, `$`, `_`)
     - Fix malformed commands
     - Check for unmatched `\begin{...}` and `\end{...}`

   **For Bibliography Errors:**
   ```
   Pattern: "WARN - I didn't find a database entry"
   ```
   - Check `Paper/references.bib` for the entry
   - Verify BibTeX syntax is correct
   - Ensure all required fields are present (author, title, year, publisher)
   - Check for special character encoding issues

   **For Missing Package Errors:**
   ```
   Pattern: "! LaTeX Error: File 'package.sty' not found"
   ```
   - Inform user that LaTeX package needs to be installed
   - Provide installation command: `tlmgr install package-name`
   - Suggest checking if TeX Live is up to date

3. **Re-compile After Each Fix:**
   ```powershell
   .\scripts\compile.ps1
   ```

4. **Repeat Until Success:**
   - If compilation still fails → Go back to step 1
   - If compilation succeeds → Proceed to Phase 7
   - **Maximum 5 iterations**: If still failing after 5 attempts, report the persistent error to user and ask for guidance

#### Step 6.4: Verify Final Output
Once compilation succeeds, verify:
- ✓ PDF file exists: `Bachelor-Thesis_Fernando_KI-Monitoring-Systeme.pdf`
- ✓ File size is reasonable (not empty or corrupted)
- ✓ No remaining warnings about undefined citations
- ✓ Compilation completed all 3 passes successfully

### Phase 7: Git Workflow

#### Step 7.1: Stage Changes
```powershell
git add Paper/chapters/02_grundlagen.tex
git add Bachelor-Thesis_Fernando_KI-Monitoring-Systeme.pdf
git add Paper/main.pdf
```

If bibliography was modified:
```powershell
git add Paper/references.bib
```

#### Step 7.2: Commit with Descriptive Message
```powershell
git commit -m "Update 2.2.3 Plattformökosysteme"
```

**Commit Message Format:**
```
Update X.X.X Section Title

- Replaced/Updated [description]
- Converted N citations
- Added M new sources (if applicable)
```

### Phase 8: Report to User
Provide summary:
```
✓ Section 2.2.3 Plattformökosysteme Updated

Citations Converted: 14
├─ Existing sources: 14
└─ New sources added: 0

Files Modified:
├─ Paper/chapters/02_grundlagen.tex
└─ references.bib (if modified)

Compilation: ✓ Successful (10.0s)
PDFs Generated:
├─ Paper/main.pdf
└─ Bachelor-Thesis_Fernando_KI-Monitoring-Systeme.pdf

Git: ✓ Committed
```

## Critical Rules

### Citation Format Rules
1. **Always use `\vglfootcite` command** (not `\cite`, `\parencite`, etc.)
2. **Page numbers:**
   - With page: `\vglfootcite[123]{Key}`
   - Without page: `\vglfootcite{Key}`
   - Multiple pages: `\vglfootcite[123\,f.]{Key}` or `\vglfootcite[123\,ff.]{Key}`
   - Page range: `\vglfootcite[29--30]{Key}`
3. **Preserve `\,` (thin space)** in page notations
4. **Place citation AFTER punctuation:** `text.\vglfootcite[10]{Key}`

### BibTeX Key Generation Rules
1. Follow existing naming convention
2. Avoid special characters (ä→ae, ö→oe, ü→ue, ß→ss)
3. Ensure uniqueness (if `Author2020` exists, use `Author2020b`)
4. Use CamelCase for multi-word last names

### Workflow Rules (NO MORE HOOKS)
1. **Complete all edits first** before compiling
2. **ALWAYS compile after finishing** (mandatory - see Phase 6)
3. **Fix compilation errors** iteratively until success
4. **Never skip compilation** - it's a mandatory step

### Git Workflow Rules
1. **Always commit PDFs** along with .tex files
2. Stage both: `Bachelor-Thesis_Fernando_KI-Monitoring-Systeme.pdf` and `Paper/main.pdf`
3. Include section number in commit message
4. Commit bibliography if new sources were added

### LaTeX Formatting Rules
1. Use `--` for en-dash (not `-` or `—`)
2. Escape special characters: `%`, `&`, `$`, `_`, `{`, `}`
3. Use `\ac{KI}` for acronyms (not plain text "KI")
4. Preserve paragraph structure (double newlines)
5. Maintain consistent indentation

## Common Error Scenarios and Solutions

### Error: String Found Multiple Times
**Cause**: `oldStr` in `str_replace` matches multiple locations

**Solution:**
- Include more surrounding context (parent section header)
- Include preceding and following paragraphs
- Verify which occurrence user wants replaced

### Error: Undefined Reference Warning
**Pattern**: `LaTeX Warning: Reference 'citekey' undefined`

**Cause**: Citation key doesn't exist in `references.bib`

**Solution:**
- Check spelling of BibTeX key
- Add missing entry to bibliography
- Run additional compilation pass

### Error: Bibliography Not Generated
**Pattern**: `WARN - I didn't find a database entry for "citekey"`

**Cause**: Mismatch between citation and bibliography

**Solution:**
- Verify citation key spelling
- Check references.bib for entry
- Ensure biber processed successfully

### Error: Hook Not Triggering
**Issue**: PDF not auto-generating after edits

**Note**: Auto-compilation hooks have been removed. You must manually compile after finishing all edits (Phase 6).

**Solution:**
- Run compilation manually: `.\scripts\compile.ps1`
- Follow Phase 6 error fix loop if needed

### Error: PDF Copy Failed
**Issue**: Cannot overwrite `Bachelor-Thesis_*.pdf`

**Cause**: File locked by PDF viewer

**Solution:**
- Close PDF viewer
- Retry compilation
- Implement retry logic in script

## FOM Hochschule Guidelines Validation

### Required Document Settings
- **Margins**: Left 4cm, Right 2cm, Top 2.5cm, Bottom 2cm
- **Font**: Times New Roman 12pt
- **Line Spacing**: 1.5
- **Required Sections**: Titelblatt, Inhaltsverzeichnis, Abbildungsverzeichnis, Abkürzungsverzeichnis, Literaturverzeichnis, Ehrenwörtliche Erklärung

### Compilation Script Checks
The `compile.ps1` script validates:
- ✓ LaTeX environment (pdflatex, biber)
- ✓ Document structure
- ✓ FOM guidelines compliance
- ✓ Acronym usage (warns about unused acronyms)

## Quick Reference: File Locations
```
BachlorsThesis/
├── .kiro/
│   └── skills/
│       └── latex-thesis-workflow/                   # This skill
├── Paper/
│   ├── main.tex                                     # Main document
│   ├── references.bib                               # Bibliography
│   ├── chapters/                                    # Chapter files
│   │   ├── 01_einleitung.tex
│   │   ├── 02_grundlagen.tex
│   │   └── ...
│   ├── main.pdf                                     # Compiled PDF
│   └── pic/                                         # Images
├── scripts/
│   └── compile.ps1                                  # Compilation script
├── HowTo/                                           # FOM guidelines
└── Bachelor-Thesis_Fernando_KI-Monitoring-Systeme.pdf  # Root PDF copy
```

## Best Practices Summary

1. ✓ **Identify target section** and chapter file correctly
2. ✓ **Analyze all citations** before converting
3. ✓ **Verify bibliography entries** exist
4. ✓ **Format LaTeX properly** (citations, paragraphs, special chars)
5. ✓ **Include sufficient context** in str_replace
6. ✓ **MANDATORY: Compile and fix errors** until successful (Phase 6)
7. ✓ **Stage PDFs** with chapter files for git
8. ✓ **Commit with descriptive message** referencing section number
9. ✓ **Report summary** to user including compilation status
10. ✓ **Never skip the compilation step** - it's mandatory

## Notes
- The `\vglfootcite` command is custom-defined in `main.tex` (lines 118-127)
- It automatically adds "Vgl." prefix and formats with "S." for pages
- Bibliography uses `authoryear` style with `biber` backend
- Ampersand (&) used between authors in citations (not "und" or "and")
- Each LaTeX compilation takes ~10 seconds
- **Auto-compilation hooks have been removed** - you must manually compile after finishing edits (Phase 6)
- **Compilation is mandatory** - never skip Phase 6
