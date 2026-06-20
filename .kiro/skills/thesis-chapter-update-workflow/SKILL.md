---
name: thesis-chapter-update-workflow
description: Guidance for updating thesis chapter content when user provides text replacements or updates for specific sections. Use when user provides content with section numbers, asks to replace sections, update chapters, or commit chapter changes with auto-generated PDFs.
---

# Thesis Chapter Update Workflow

## Purpose
This skill provides guidance for updating thesis chapter content when the user provides text replacements or updates for specific sections.

## Context
Use this skill when:
- User provides text content to replace a section in a chapter
- User mentions updating section numbers (e.g., "2.2.1", "3.1.2")
- User provides content with section headings to be integrated
- User asks to commit changes after chapter updates

## Key Concepts

### Chapter File Structure
Thesis chapters are located in `Paper/chapters/`:
- `01_einleitung.tex` - Introduction
- `02_grundlagen.tex` - Theoretical foundations
- `03_monitoring_systeme.tex` - Monitoring systems
- `04_implikationen.tex` - Implications
- `05_kritische_betrachtung.tex` - Critical analysis
- `06_fazit.tex` - Conclusion

### Section Numbering
- Chapters use `\chapter{}` for top-level (e.g., Chapter 2)
- Sections use `\section{}` (e.g., 2.1)
- Subsections use `\subsection{}` (e.g., 2.2.1)
- Sub-subsections use `\subsubsection{}` (e.g., 2.2.1.1)

### Auto-Generated PDFs
When chapters are updated, the LaTeX compilation hook automatically generates:
- `Paper/main.pdf` - Main thesis PDF
- `Bachelor-Thesis_Fernando_KI-Monitoring-Systeme.pdf` - Root-level copy

**These PDFs should ALWAYS be committed along with chapter updates.**

## Workflow Pattern

### 1. Identify Target Section
When user provides content like:
```
2.2.1 Funktionale Architektur KI-gestützter Monitoring-Systeme
Die funktionale Architektur...
```

Extract:
- Chapter number: `2` → `02_grundlagen.tex`
- Section path: `2.2.1` → subsection within section 2.2
- Section title: `Funktionale Architektur KI-gestützter Monitoring-Systeme`

### 2. Find Existing Section
Search for the section in the target chapter file:
```powershell
grep -n "\\subsection{.*}" Paper/chapters/02_grundlagen.tex
```

If section exists, prepare to replace it. If not, determine insertion point.

### 3. Handle Duplicates
If the same subsection title appears multiple times:
- Ask user which occurrence to replace
- Use surrounding context to make unique match
- Consider replacing within specific parent section

### 4. Format LaTeX Content
Convert provided text to proper LaTeX format:
- Add `\subsection{Title}` header
- Preserve paragraphs (double newlines in LaTeX)
- Keep citation format: `(vgl. Author Year, S. Page)` → `\vglfootcite[Page]{CiteKey}`
- Maintain special characters and formatting

### 5. Replace Content
Use `str_replace` tool with:
- **oldStr**: Complete original section including header and content
- **newStr**: Complete new section with proper LaTeX formatting
- Include enough context (surrounding paragraphs) to ensure unique match

### 6. Stage Generated PDFs
After successful replacement, the compilation hook auto-generates PDFs:
```powershell
git add Bachelor-Thesis_Fernando_KI-Monitoring-Systeme.pdf Paper/main.pdf
```

### 7. Commit Changes
Commit with descriptive message referencing section number:
```powershell
git commit -m "Update 2.2.1 Funktionale Architektur KI-gestützter Monitoring-Systeme"
```

## Implementation Examples

### Example 1: Simple Subsection Replace
```powershell
# User provides: "Replace 2.2.1 with this content..."
# 1. Identify file: 02_grundlagen.tex
# 2. Find section: \subsection{Systemarchitekturen}
# 3. Replace with new \subsection{Funktionale Architektur...}
# 4. PDFs auto-generate via hook
# 5. Stage PDFs: git add *.pdf
# 6. Commit: git commit -m "Update 2.2.1 ..."
```

### Example 2: Handle Duplicates
```powershell
# If \subsection{Same Title} appears twice:
# 1. Read surrounding context for both occurrences
# 2. Match parent section (e.g., within \section{Digitale Informationssysteme})
# 3. Include parent section in oldStr for unique match
```

### Example 3: Revert and Replace
```powershell
# If previous attempt failed:
git checkout Paper/chapters/02_grundlagen.tex  # Revert file
# Then retry replacement with corrected matching
```

## Common Scenarios

### User Says "Replace section 2.2.1"
1. Parse section number: `2.2.1` → chapter 2, subsection
2. Open `Paper/chapters/02_grundlagen.tex`
3. Find `\subsection{...}` that matches the section number context
4. Replace entire subsection content
5. Commit with PDFs

### User Says "We worked on 2.2.2, not 2.2.1"
- Correct the commit message to reference actual section
- Use `git commit --amend -m "Updated message"` if needed

### User Says "Commit the changes"
1. Check `git status` for modified files
2. Stage chapter file (if not already staged)
3. **Always add generated PDFs**: `git add *.pdf`
4. Commit with section reference in message

### User Says "Revert the file first"
```powershell
git checkout c:\development\PrivProjects\BachlorsThesis\Paper\chapters\XX_chapter.tex
```

## Error Handling

### Multiple Matches Error
**Error**: `String found multiple times`

**Solution**:
- Include more surrounding context in oldStr
- Include parent section heading
- Verify which occurrence user wants replaced

### Missing Section
**Error**: Section not found in file

**Solution**:
- Verify section number mapping to file
- Check if section exists or needs to be inserted
- Ask user for clarification on insertion point

### PDF Not Generated
**Issue**: Hook didn't trigger compilation

**Solution**:
- Manually trigger: `.\scripts\compile.ps1`
- Check hook is enabled: `.kiro/hooks/latex-compile-after-tool-edit.kiro.hook`

## Git Workflow Rules

### Always Include Generated PDFs
```powershell
# After any chapter modification:
git add Bachelor-Thesis_Fernando_KI-Monitoring-Systeme.pdf
git add Paper/main.pdf
git add Paper/chapters/*.tex  # The modified chapter
git commit -m "Update X.X.X Section Title"
```

### Commit Message Format
```
Update X.X.X Section Title

- Replaced [old content description]
- Updated [specific changes]
```

Example:
```
Update 2.2.1 Funktionale Architektur KI-gestützter Monitoring-Systeme

- Replaced "Systemarchitekturen" subsection
- Added functional architecture components description
```

## Best Practices

1. **Always verify section number** before replacing
2. **Read current content** to understand context
3. **Include sufficient context** in str_replace for unique matching
4. **Stage PDFs immediately** after successful replacement
5. **Use descriptive commit messages** with section references
6. **Revert on failure** rather than attempting incremental fixes
7. **Confirm with user** when section identification is ambiguous
8. **Preserve LaTeX formatting** (citations, special characters, structure)

## When to Use This Skill

Activate this skill when:
- User provides text content with section numbers (e.g., "2.2.1 Title...")
- User says "replace section X.X.X with this"
- User says "update chapter content"
- User asks to commit chapter changes
- User mentions thesis sections or subsections
- User provides German academic text with citations

## Related Skills

- `latex-thesis-compilation` - For PDF generation details
- Hooks: `latex-compile-after-tool-edit.kiro.hook` - Auto-compilation trigger
