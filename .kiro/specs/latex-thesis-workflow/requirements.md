# Requirements Document

## Introduction

This document specifies requirements for an automated LaTeX thesis compilation workflow system for a Bachelor's thesis project at FOM Hochschule, Studienzentrum Frankfurt. The system automates the compilation of LaTeX documents following FOM Hochschule guidelines, including bibliography management with biber, PDF generation, and file organization.

## Glossary

- **Thesis_System**: The automated LaTeX compilation workflow system
- **Compiler**: The pdflatex executable that processes LaTeX source files
- **Bibliography_Processor**: The biber tool that processes bibliography references
- **Main_Document**: The LaTeX source file located at Paper/main.tex
- **Bibliography_File**: The BibTeX file containing references at Paper/references.bib
- **Output_PDF**: The compiled PDF file named Bachelor-Thesis_Fernando_KI-Monitoring-Systeme.pdf
- **Working_Directory**: The Paper/ directory where compilation occurs
- **Root_Directory**: The repository root directory where the final PDF is copied
- **Compilation_Pass**: A single execution of pdflatex on the Main_Document
- **Auxiliary_Files**: Temporary files generated during compilation (.aux, .bbl, .bcf, .blg, .log, .out, .toc, .lof, .lot, .run.xml, .equ)
- **FOM_Guidelines**: The formal thesis guidelines documents located in HowTo/ directory
- **LaTeX_Distribution**: TeX Live 2026 or later installation
- **Required_Packages**: LaTeX packages specified in collection-latexextra, collection-fontsrecommended, babel-german, hyphen-german

## Requirements

### Requirement 1: LaTeX Document Compilation

**User Story:** As a thesis author, I want to compile my LaTeX document automatically, so that I can generate a PDF without manual intervention.

#### Acceptance Criteria

1. WHEN the Main_Document exists at Paper/main.tex, THE Thesis_System SHALL execute the Compiler with -interaction=nonstopmode flag
2. THE Thesis_System SHALL execute three sequential Compilation_Passes to ensure correct cross-references and table of contents
3. WHEN any Compilation_Pass fails, THE Thesis_System SHALL capture error messages and report them to the user
4. THE Thesis_System SHALL preserve the Working_Directory context during compilation
5. WHEN compilation completes successfully, THE Thesis_System SHALL verify that Paper/main.pdf exists

### Requirement 2: Bibliography Processing

**User Story:** As a thesis author, I want bibliography references processed automatically, so that citations appear correctly in my thesis.

#### Acceptance Criteria

1. WHEN the first Compilation_Pass completes, THE Thesis_System SHALL execute the Bibliography_Processor on the main document
2. THE Bibliography_Processor SHALL process the Bibliography_File at Paper/references.bib
3. WHEN the Bibliography_Processor encounters errors, THE Thesis_System SHALL capture and report error messages
4. THE Thesis_System SHALL execute two additional Compilation_Passes after Bibliography_Processor completes to integrate references
5. FOR ALL valid citation keys in the Main_Document, THE Thesis_System SHALL ensure they resolve to bibliography entries after compilation

### Requirement 3: Output File Management

**User Story:** As a thesis author, I want the compiled PDF copied to the repository root with the correct filename, so that I can easily access and share my thesis.

#### Acceptance Criteria

1. WHEN compilation completes successfully, THE Thesis_System SHALL copy Paper/main.pdf to the Root_Directory
2. THE Thesis_System SHALL rename the copied file to Bachelor-Thesis_Fernando_KI-Monitoring-Systeme.pdf
3. IF the Output_PDF already exists in the Root_Directory, THE Thesis_System SHALL overwrite it
4. WHEN the copy operation completes, THE Thesis_System SHALL display a success message indicating the Output_PDF location
5. IF the copy operation fails, THE Thesis_System SHALL report an error and retain Paper/main.pdf

### Requirement 4: LaTeX Environment Prerequisites Validation

**User Story:** As a thesis author, I want to verify that my LaTeX environment is properly configured, so that compilation will succeed.

#### Acceptance Criteria

1. THE Thesis_System SHALL verify that the LaTeX_Distribution is installed and accessible
2. THE Thesis_System SHALL verify that the Compiler (pdflatex) is available in the system PATH
3. THE Thesis_System SHALL verify that the Bibliography_Processor (biber) is available in the system PATH
4. WHEN Required_Packages are missing, THE Thesis_System SHALL report which packages need installation
5. THE Thesis_System SHALL provide installation instructions for missing Required_Packages

### Requirement 5: FOM Guideline Compliance Validation

**User Story:** As a thesis author, I want to validate my document against FOM guidelines, so that my thesis meets university requirements.

#### Acceptance Criteria

1. THE Thesis_System SHALL verify that page margins match FOM guidelines (left 4cm, right 2cm, top 2.5cm, bottom 2cm)
2. THE Thesis_System SHALL verify that font settings use Times New Roman 12pt with 1.5 line spacing
3. THE Thesis_System SHALL verify that the Main_Document includes required front matter sections (Titelblatt, Inhaltsverzeichnis, Abbildungsverzeichnis, Abkürzungsverzeichnis, Formelverzeichnis, Tabellenverzeichnis)
4. THE Thesis_System SHALL verify that the Main_Document includes required back matter sections (Literaturverzeichnis, Ehrenwörtliche Erklärung)
5. WHEN guideline violations are detected, THE Thesis_System SHALL report specific non-compliant elements with references to FOM_Guidelines sections

### Requirement 6: Document Structure Parsing and Validation

**User Story:** As a thesis author, I want the system to parse my LaTeX document structure, so that I can identify structural issues before compilation.

#### Acceptance Criteria

1. THE Thesis_System SHALL parse the Main_Document and extract all \input and \include directives
2. THE Thesis_System SHALL verify that all referenced chapter files exist in the chapters/ directory
3. WHEN a referenced file is missing, THE Thesis_System SHALL report the missing file path
4. THE Thesis_System SHALL verify that the Bibliography_File exists and is readable
5. THE Thesis_System SHALL parse the Bibliography_File and report any syntax errors with line numbers

### Requirement 7: Auxiliary File Management

**User Story:** As a thesis author, I want auxiliary compilation files managed automatically, so that my working directory stays organized.

#### Acceptance Criteria

1. THE Thesis_System SHALL preserve Auxiliary_Files during compilation for incremental builds
2. WHERE a clean build is requested, THE Thesis_System SHALL remove all Auxiliary_Files before compilation
3. THE Thesis_System SHALL identify Auxiliary_Files by extensions: .aux, .bbl, .bcf, .blg, .log, .out, .toc, .lof, .lot, .run.xml, .equ, .fls, .fdb_latexmk, .synctex.gz
4. WHEN removing Auxiliary_Files, THE Thesis_System SHALL preserve the Main_Document, Bibliography_File, and source .tex files
5. THE Thesis_System SHALL report the count of Auxiliary_Files removed

### Requirement 8: Compilation Error Diagnostics

**User Story:** As a thesis author, I want detailed error diagnostics when compilation fails, so that I can quickly identify and fix issues.

#### Acceptance Criteria

1. WHEN the Compiler reports errors, THE Thesis_System SHALL parse the .log file and extract error messages
2. THE Thesis_System SHALL report error messages with file paths and line numbers
3. THE Thesis_System SHALL identify common LaTeX errors (undefined references, missing packages, syntax errors, overfull hboxes)
4. WHEN the Bibliography_Processor reports errors, THE Thesis_System SHALL parse the .blg file and extract error messages
5. THE Thesis_System SHALL categorize errors by severity (critical errors that prevent compilation, warnings that produce output)

### Requirement 9: Incremental Compilation Detection

**User Story:** As a thesis author, I want the system to detect when incremental compilation is safe, so that I can save time during iterative edits.

#### Acceptance Criteria

1. THE Thesis_System SHALL track modification timestamps of the Main_Document and all chapter files
2. WHEN source files have not changed since last compilation, THE Thesis_System SHALL report that Output_PDF is up-to-date
3. WHEN the Bibliography_File has changed, THE Thesis_System SHALL execute full compilation with Bibliography_Processor
4. WHEN only chapter files have changed, THE Thesis_System SHALL execute full compilation
5. WHERE incremental compilation is requested, THE Thesis_System SHALL perform only one Compilation_Pass when sufficient

### Requirement 10: Compilation Progress Reporting

**User Story:** As a thesis author, I want real-time feedback during compilation, so that I know the system is working and can estimate completion time.

#### Acceptance Criteria

1. WHEN each Compilation_Pass starts, THE Thesis_System SHALL display a progress message indicating the current pass number
2. WHEN the Bibliography_Processor starts, THE Thesis_System SHALL display a progress message indicating bibliography processing
3. THE Thesis_System SHALL display completion status for each compilation stage (pass 1, biber, pass 2, pass 3, file copy)
4. WHEN compilation completes successfully, THE Thesis_System SHALL display total compilation time
5. THE Thesis_System SHALL display error count and warning count after each stage

### Requirement 11: Cross-Platform Path Handling

**User Story:** As a thesis author, I want the system to work on Windows, so that I can compile my thesis on my development machine.

#### Acceptance Criteria

1. THE Thesis_System SHALL use platform-appropriate path separators when constructing file paths
2. THE Thesis_System SHALL resolve relative paths correctly from the Working_Directory
3. THE Thesis_System SHALL handle Windows path formats (drive letters and backslashes)
4. WHEN accessing system executables, THE Thesis_System SHALL search the system PATH using platform conventions
5. THE Thesis_System SHALL handle file paths with spaces correctly by quoting paths in shell commands

### Requirement 12: LaTeX Package Detection and Reporting

**User Story:** As a thesis author, I want the system to detect missing LaTeX packages, so that I can install them before compilation fails.

#### Acceptance Criteria

1. WHEN the Compiler reports missing packages in the .log file, THE Thesis_System SHALL extract package names
2. THE Thesis_System SHALL report missing packages with installation commands for TeX Live
3. THE Thesis_System SHALL detect packages required by the Main_Document preamble
4. THE Thesis_System SHALL verify that critical packages (babel-german, biblatex, geometry, setspace, titlesec) are available
5. WHEN package installation instructions are displayed, THE Thesis_System SHALL format them as executable tlmgr commands

