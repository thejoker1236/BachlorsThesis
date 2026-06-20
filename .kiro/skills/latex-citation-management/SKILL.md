---
name: latex-citation-management
description: Comprehensive workflow for integrating new text with citations into the thesis. Use when user provides text with inline citations that need to be converted to footnote format, when adding new sources to references.bib, or when integrating research notes with multiple citations.
---

# LaTeX Citation Management & Text Integration

## Purpose
This skill provides a comprehensive workflow for integrating new text with citations into the thesis, including:
- Converting inline citations to footnote format
- Checking existing bibliography entries
- Adding new sources to `references.bib`
- Ensuring consistent citation style throughout the document

## When to Use
- User provides new text with inline citations (e.g., "(vgl. Author 2016, S. 123)")
- User pastes text sections that need citation formatting
- Adding new chapter content with multiple sources
- Integrating research notes into the thesis

## Complete Workflow

### Phase 1: Preparation (Disable Hook)
Before starting any text editing, disable the auto-compilation hook to prevent multiple unnecessary compilations.

**Action:**
1. Read `.kiro/hooks/latex-compile-after-tool-edit.kiro.hook`
2. Change `"enabled": true` to `"enabled": false`
3. Save the file

### Phase 2: Analysis of Provided Text

#### Step 2.1: Identify All Citations in User Text
Parse the user's provided text for citation patterns:
- `(vgl. Author 2016, S. 123)`
- `(vgl. Author, Author2 und Author3 2020, S. 45)`
- `(vgl. Author 2018)`
- `(Author 2021, S. 10\,f.)`

Create a list of all citations found.

#### Step 2.2: Read Existing Bibliography
**Action:**
1. Read `Paper/references.bib`
2. Parse all `@book`, `@article`, `@report`, etc. entries
3. Extract BibTeX keys (e.g., `Laudon2016`, `Pasquale2015`)
4. Create mapping: Author(Year) → BibTeX Key

**Example Mapping:**
```
Laudon, Laudon und Elragal 2016 → Laudon2016
Russell und Norvig 2010 → RussellNorvig2010
Pasquale 2015 → Pasquale2015
Goodfellow, Bengio und Courville 2016 → Goodfellow2016
```

#### Step 2.3: Check Existing Citation Style
**Action:**
1. Read one of the existing chapter files (e.g., `chapters/01_einleitung.tex`)
2. Identify the citation command format used
3. Verify it matches: `\vglfootcite[page]{BibTeXKey}`

**Expected Format:**
- `\vglfootcite[30]{Laudon2016}` → Produces: "Vgl. Laudon, Laudon & Elragal (2016), S. 30."
- `\vglfootcite[148]{Laudon2016}` → Produces: "Vgl. Laudon, Laudon & Elragal (2016), S. 148."
- `\vglfootcite[12\,f.]{Author2020}` → Produces: "Vgl. Author (2020), S. 12 f."

### Phase 3: Source Management

#### Step 3.1: Match Citations to Existing BibTeX Entries
For each citation found in user's text:
1. Extract author name(s) and year
2. Try to match against existing BibTeX keys
3. Mark as FOUND or MISSING

**Example:**
```
Citation: (vgl. Laudon, Laudon und Elragal 2016, S. 148)
→ Author pattern: "Laudon, Laudon und Elragal"
→ Year: 2016
→ Search in references.bib: FOUND → Laudon2016
→ Action: Use \vglfootcite[148]{Laudon2016}
```

#### Step 3.2: Identify Missing Sources
For citations marked as MISSING:
1. Create a list of sources that need to be added
2. Ask user to provide complete bibliographic information for each missing source

**Information needed for each missing source:**
- **For books:**
  - Authors (full names)
  - Title
  - Year
  - Edition (if applicable)
  - Publisher
  - Location

- **For articles:**
  - Authors (full names)
  - Title
  - Journal name
  - Year
  - Volume
  - Number
  - Pages
  - DOI (if available)

#### Step 3.3: Generate BibTeX Keys for New Sources
For new sources, create BibTeX keys following the existing convention:
- Single author: `LastName+Year` (e.g., `Pasquale2015`)
- Two authors: `LastName1LastName2+Year` (e.g., `RussellNorvig2010`)
- Three+ authors: `FirstAuthorLastName+Year` (e.g., `Laudon2016`)

#### Step 3.4: Add New Entries to references.bib
**Action:**
1. Read `Paper/references.bib`
2. Determine the appropriate section (e.g., `% Kapitel 2 — ...`)
3. Format new BibTeX entries according to existing style
4. Insert entries in alphabetical order within the section
5. Save the updated `references.bib`

**Example New Entry:**
```bibtex
@article{Mittelstadt2016,
  author    = {Mittelstadt, Brent Daniel and Allo, Patrick and Taddeo, Mariarosaria and Wachter, Sandra and Floridi, Luciano},
  title     = {The Ethics of Algorithms: Mapping the Debate},
  journal   = {Big Data \& Society},
  year      = {2016},
  volume    = {3},
  number    = {2},
  pages     = {1--21},
  doi       = {10.1177/2053951716679679}
}
```

### Phase 4: Citation Conversion

#### Step 4.1: Convert All Inline Citations to Footnotes
For each citation in the user's provided text:

**Pattern Recognition:**
```
(vgl. Author(s) Year, S. Page) 
→ \vglfootcite[Page]{BibTeXKey}
```

**Conversion Examples:**
```
(vgl. Laudon, Laudon und Elragal 2016, S. 148)
→ \vglfootcite[148]{Laudon2016}

(vgl. Russell und Norvig 2010, S. 34)
→ \vglfootcite[34]{RussellNorvig2010}

(vgl. Pasquale 2015, S. 6)
→ \vglfootcite[6]{Pasquale2015}

(vgl. Author 2020, S. 12\,f.)
→ \vglfootcite[12\,f.]{Author2020}

(vgl. Author 2018)
→ \vglfootcite{Author2018}
```

#### Step 4.2: Handle Special Page Notation
Preserve German academic page notation:
- `S. 12\,f.` (Seite 12 folgende) = page 12 and following
- `S. 12\,ff.` (Seite 12 fortfolgende) = page 12 and several following
- `S. 1\,ff.` (Seite 1 fortfolgende) = from page 1 onwards

**Keep the `\,` (thin space) and `f.`/`ff.` notation intact!**

### Phase 5: Text Integration

#### Step 5.1: Insert Text into Target Chapter File
1. Identify the target chapter file (user will specify)
2. Locate the exact insertion point (section, subsection)
3. Insert the formatted text with converted citations
4. Ensure proper LaTeX formatting (paragraph breaks, special characters)

#### Step 5.2: Verify No Duplicate Citations
Check that the same citation doesn't appear twice in a sentence:
```
❌ WRONG: Text text.\vglfootcite[30]{Laudon2016} More text (vgl. Laudon 2016, S. 30).
✓ CORRECT: Text text.\vglfootcite[30]{Laudon2016} More text.
```

### Phase 6: Validation & Compilation

#### Step 6.1: Verify All BibTeX Keys Exist
Cross-check all used `\vglfootcite` commands against `references.bib`:
1. Extract all BibTeX keys used in citations
2. Verify each key exists in `references.bib`
3. Report any missing keys

#### Step 6.2: Re-Enable Hook
**Action:**
1. Read `.kiro/hooks/latex-compile-after-tool-edit.kiro.hook`
2. Change `"enabled": false` back to `"enabled": true`
3. Save the file

#### Step 6.3: Final Compilation
Run the compilation script:
```powershell
.\scripts\compile.ps1
```

**Check compilation output for:**
- ✓ All citations resolved (no "undefined reference" warnings)
- ✓ Bibliography generated correctly
- ✓ PDF created successfully

### Phase 7: Report to User

Provide a summary:
```
✓ Text Integration Complete

Citations Converted: 15
├─ Existing sources: 12
└─ New sources added: 3

New BibTeX Entries Added:
├─ Author2023 (Book)
├─ Smith2024 (Article)
└─ Johnson2022 (Report)

Files Modified:
├─ Paper/chapters/02_grundlagen.tex (text + citations)
└─ Paper/references.bib (+3 entries)

Compilation: ✓ Successful
```

## Example Complete Workflow

### User Input:
```
"Bitte füge folgenden Text in Abschnitt 2.3 ein:

Die Analyse zeigt, dass algorithmische Systeme zunehmend 
in Entscheidungsprozesse eingreifen (vgl. O'Neil 2016, S. 29). 
Dabei entstehen systematische Verzerrungen, die gesellschaftliche 
Ungleichheiten verstärken können (vgl. Noble 2018, S. 1\,ff.)."
```

### Agent Actions:

**1. Disable Hook**
```
Modified: .kiro/hooks/latex-compile-after-tool-edit.kiro.hook
"enabled": true → "enabled": false
```

**2. Analyze Citations**
```
Found citations:
- (vgl. O'Neil 2016, S. 29)
- (vgl. Noble 2018, S. 1\,ff.)
```

**3. Check references.bib**
```
Searching for: O'Neil 2016
→ FOUND: ONeil2016

Searching for: Noble 2018
→ MISSING: Need bibliographic info
```

**4. Request Missing Source Info**
```
"The citation 'Noble 2018' was not found in references.bib.
Please provide complete bibliographic information:
- Full author name(s)
- Complete title
- Publisher
- Location
- Year
- Any additional details (edition, pages, DOI, etc.)"
```

**5. User Provides Info**
```
Author: Safiya Umoja Noble
Title: Algorithms of Oppression: How Search Engines Reinforce Racism
Year: 2018
Publisher: NYU Press
Location: New York
```

**6. Add to references.bib**
```bibtex
@book{Noble2018,
  author    = {Noble, Safiya Umoja},
  title     = {Algorithms of Oppression: How Search Engines Reinforce Racism},
  year      = {2018},
  publisher = {NYU Press},
  address   = {New York}
}
```

**7. Convert Citations**
```
Original text:
"Die Analyse zeigt, dass algorithmische Systeme zunehmend 
in Entscheidungsprozesse eingreifen (vgl. O'Neil 2016, S. 29). 
Dabei entstehen systematische Verzerrungen, die gesellschaftliche 
Ungleichheiten verstärken können (vgl. Noble 2018, S. 1\,ff.)."

Converted text:
"Die Analyse zeigt, dass algorithmische Systeme zunehmend 
in Entscheidungsprozesse eingreifen.\vglfootcite[29]{ONeil2016} 
Dabei entstehen systematische Verzerrungen, die gesellschaftliche 
Ungleichheiten verstärken können.\vglfootcite[1\,ff.]{Noble2018}"
```

**8. Insert into Chapter File**
```
Modified: Paper/chapters/02_grundlagen.tex
Added text to section 2.3
```

**9. Re-Enable Hook**
```
Modified: .kiro/hooks/latex-compile-after-tool-edit.kiro.hook
"enabled": false → "enabled": true
```

**10. Compile**
```
Compilation successful ✓
New PDF generated ✓
```

**11. Report**
```
✓ Text Integration Complete

Citations Converted: 2
├─ Existing sources: 1 (ONeil2016)
└─ New sources added: 1 (Noble2018)

New BibTeX Entries Added:
└─ Noble2018 (Book)

Files Modified:
├─ Paper/chapters/02_grundlagen.tex
└─ Paper/references.bib

Compilation: ✓ Successful
```

## Critical Rules

### Citation Matching Rules
1. **Author name matching:**
   - Ignore spaces and punctuation
   - Handle "und" / "and" / "&"
   - Match abbreviated vs. full first names

2. **Year matching:**
   - Must match exactly
   - If multiple entries for same author+year, ask user to clarify

3. **Ambiguity resolution:**
   - If uncertain about a match, ask user to confirm
   - Show the BibTeX key you plan to use

### BibTeX Key Generation Rules
1. Follow existing naming convention in references.bib
2. Avoid special characters (ä→ae, ö→oe, ü→ue, ß→ss)
3. Ensure uniqueness (if `Author2020` exists, use `Author2020b`)
4. Use CamelCase for multi-word last names

### Citation Format Rules
1. **Always use `\vglfootcite` command** (not `\cite`, `\parencite`, etc.)
2. **Page numbers:**
   - With page: `\vglfootcite[123]{Key}`
   - Without page: `\vglfootcite{Key}`
   - Multiple pages: `\vglfootcite[123\,f.]{Key}` or `\vglfootcite[123\,ff.]{Key}`
3. **Preserve `\,` (thin space)** in page notations
4. **Place citation AFTER punctuation:** `text.\vglfootcite[10]{Key}` NOT `text\vglfootcite[10]{Key}.`

### Quality Checks Before Compilation
1. ✓ All inline citations converted
2. ✓ All BibTeX keys exist in references.bib
3. ✓ No duplicate citations in same sentence
4. ✓ Proper punctuation placement
5. ✓ Special characters escaped (%, &, $, etc.)
6. ✓ Hook re-enabled

## Benefits
- **Consistency**: All citations follow the same footnote format
- **Completeness**: All sources are properly cataloged in references.bib
- **Efficiency**: Bulk operations without repeated compilations
- **Quality**: Systematic verification prevents missing citations
- **Maintainability**: Clean BibTeX database for future reference

## Common Issues & Solutions

### Issue 1: Citation Not Found in references.bib
**Solution:** Ask user for complete bibliographic information, create BibTeX entry

### Issue 2: Ambiguous Author Match
**Example:** "Schmidt 2020" could match `Schmidt2020` or `SchmidtMueller2020`
**Solution:** Present options to user and ask for clarification

### Issue 3: Special Characters in Names
**Example:** "Müller 2019"
**Solution:** Check for both `Mueller2019` and `Muller2019` in references.bib

### Issue 4: Missing Page Numbers
**Example:** "(vgl. Author 2020)"
**Solution:** Use `\vglfootcite{Author2020}` (without page parameter)

### Issue 5: Compilation Fails After Integration
**Actions:**
1. Check for undefined BibTeX keys
2. Verify all special LaTeX characters are escaped
3. Check for broken paragraph structure
4. Run `biber main` manually if needed

## File Locations Reference
- Bibliography: `Paper/references.bib`
- Hook file: `.kiro/hooks/latex-compile-after-tool-edit.kiro.hook`
- Chapter files: `Paper/chapters/*.tex`
- Compilation script: `scripts/compile.ps1`
- Main document: `Paper/main.tex`

## Additional Notes
- The `\vglfootcite` command is custom-defined in `main.tex` (lines 118-127)
- It automatically adds "Vgl." prefix and formats page numbers with "S."
- The bibliography uses `authoryear` style with `biber` backend
- Ampersand (&) is used between authors in citations (not "und" or "and")
