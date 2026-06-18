# Implementation Plan: LaTeX Thesis Workflow

## Overview

This implementation plan breaks down the PowerShell-based LaTeX thesis compilation automation system into discrete coding tasks. The system orchestrates multi-pass compilation (pdflatex → biber → pdflatex → pdflatex), validates FOM guideline compliance, provides error diagnostics, and manages file operations. The implementation follows a bottom-up approach, building foundational modules first, then integrating them into the orchestrator.

## Summary of Completed Work

### ✅ Completed Tasks:
1. **Task 1** - Project structure and core setup
2. **Task 2.1** - Environment Validator (integrated into compile.ps1)
3. **Task 6.1** - Progress Reporter (integrated into compile.ps1)
4. **Task 7.1** - Error Diagnostics (basic log parsing integrated)
5. **Task 5.1** (partial) - File Manager (-Clean flag implemented)
6. **Task 11.1** - Compilation Engine (core workflow)
7. **Task 12.1** (enhanced) - Main Orchestrator with CLI parameters
8. **Task 14.1** - Windows path handling
9. **Task 15.1** (partial) - CLI parameter parsing (-Clean, -Incremental, -ValidateOnly)

### 🚧 High-Priority Remaining Tasks:
- **Task 3.1** - Document Parser (validate structure before compilation)
- **Task 10.1** - Incremental Build Detector (enhanced timestamp checking)
- **Task 16.1** - Enhanced error formatting with line numbers
- **Task 16.2** - Comprehensive logging

### 📊 Optional Tasks (can skip for MVP):
- All test tasks (marked with *)
- Task 8 - FOM Guideline Validator
- Configuration file loading (currently using defaults)

---

## Tasks

- [x] 1. Create project structure and core type definitions
  - Create scripts/ directory if not exists
  - Define PowerShell classes for data models: CompilationConfiguration, FOMGuidelines, ValidateResult, DocumentStructure, CompilationResult, DiagnosticReport, LaTeXError, ComplianceReport, ComplianceViolation, BuildDecision
  - Create config.json with default configuration
  - Set up module structure with .psm1 files
  - _Requirements: 1.1, 1.4, 4.1_

- [ ] 2. Implement Environment Validator Module
  - [x] 2.1 Create EnvironmentValidator.psm1 module
    - Implement Test-LaTeXEnvironment function
    - Implement Test-ExecutableInPath helper to check for pdflatex and biber
    - Implement Test-PackageInstallation helper using kpsewhich
    - Implement Get-InstallationInstructions to generate tlmgr commands
    - Return ValidateResult object with missing executables/packages
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 12.1, 12.2, 12.5_

  - [ ]* 2.2 Write unit tests for Environment Validator
    - Test valid environment with all prerequisites
    - Test missing pdflatex executable
    - Test missing biber executable
    - Test missing required packages
    - Test installation instructions generation
    - _Requirements: 4.1, 4.2, 4.3, 4.4_

- [ ] 3. Implement Document Parser Module
  - [ ] 3.1 Create DocumentParser.psm1 module
    - Implement Get-DocumentStructure function
    - Implement Parse-InputDirectives to extract \input{} and \include{} directives using regex
    - Implement Validate-FileReferences to check file existence
    - Implement Parse-BibliographyFile to validate .bib syntax
    - Return DocumentStructure object with chapter files, bibliography file, package usage
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5, 12.3_

  - [ ]* 3.2 Write unit tests for Document Parser
    - Test valid main.tex with chapter includes
    - Test missing chapter file detection
    - Test invalid bibliography file syntax
    - Test circular include dependencies
    - Test package extraction from preamble
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 6.5_

- [ ] 4. Checkpoint - Ensure foundational modules are testable
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 5. Implement File Manager Module
  - [ ] 5.1 Create FileManager.psm1 module
    - Implement Clear-AuxiliaryFiles function to remove files by extension
    - Implement Get-AuxiliaryFiles helper to enumerate auxiliary files
    - Implement Remove-SafelyAuxiliaryFiles to preserve source files
    - Implement Copy-OutputPDF function with retry logic
    - Implement Copy-WithRetry helper for robust file copy
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5, 3.1, 3.2, 3.3, 3.5_

  - [ ]* 5.2 Write unit tests for File Manager
    - Test auxiliary file cleanup with mock files
    - Test source file preservation during cleanup
    - Test PDF copy with rename
    - Test copy retry logic on locked files
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 3.1_

- [ ] 6. Implement Progress Reporter Module
  - [ ] 6.1 Create ProgressReporter.psm1 module
    - Implement Write-CompilationProgress function for stage messages
    - Implement Write-CompilationSummary function for completion summary
    - Implement Write-StageHeader helper for formatted banners
    - Implement Write-SuccessMessage with PDF location
    - Implement Write-ErrorSummary for categorized errors
    - Use Write-Host with color-coded output
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

  - [ ]* 6.2 Write unit tests for Progress Reporter
    - Test stage header formatting
    - Test success message display
    - Test error summary formatting
    - Test compilation summary with timing
    - _Requirements: 10.1, 10.2, 10.3, 10.4_

- [ ] 7. Implement Error Diagnostics Module
  - [ ] 7.1 Create ErrorDiagnostics.psm1 module
    - Implement Get-CompilationDiagnostics function
    - Implement Parse-LogFile to extract errors from .log using regex patterns
    - Implement Parse-BlgFile to extract bibliography errors from .blg
    - Implement Classify-ErrorType to categorize (undefined reference, missing package, syntax error, overfull hbox)
    - Implement Format-ErrorMessage for user-friendly descriptions
    - Return DiagnosticReport with categorized errors and warnings
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5, 12.1_

  - [ ]* 7.2 Write unit tests for Error Diagnostics
    - Test .log file parsing with sample error logs
    - Test undefined reference extraction
    - Test missing package error detection
    - Test bibliography error parsing from .blg
    - Test error severity classification
    - _Requirements: 8.1, 8.2, 8.3, 8.4, 8.5_

- [ ] 8. Implement Guideline Validator Module
  - [ ] 8.1 Create GuidelineValidator.psm1 module
    - Implement Test-FOMCompliance function
    - Implement Validate-PageGeometry to check margins using geometry package settings
    - Implement Validate-FontSettings to verify Times New Roman 12pt and 1.5 spacing
    - Implement Validate-DocumentStructure to check required sections
    - Implement Parse-GeometryPackage to extract margin settings from preamble
    - Return ComplianceReport with violations and guideline references
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

  - [ ]* 8.2 Write unit tests for Guideline Validator
    - Test compliant document validation
    - Test non-compliant margin detection
    - Test missing front matter section detection
    - Test incorrect font specification detection
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5_

- [ ] 9. Checkpoint - Ensure all validation and diagnostic modules are complete
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 10. Implement Incremental Build Detector Module
  - [ ] 10.1 Create IncrementalBuildDetector.psm1 module
    - Implement Test-CompilationRequired function
    - Implement Get-SourceFileTimestamps to collect modification times
    - Implement Get-OutputTimestamp for PDF creation time
    - Implement Compare-Timestamps to determine if rebuild needed
    - Implement Detect-BibliographyChanges to check .bib modifications
    - Return BuildDecision with rebuild requirements and reason
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

  - [ ]* 10.2 Write unit tests for Incremental Build Detector
    - Test unchanged sources detection
    - Test modified chapter file detection
    - Test modified bibliography detection
    - Test timestamp comparison logic
    - _Requirements: 9.1, 9.2, 9.3, 9.4_

- [x] 11. Implement Compilation Engine Module
  - [x] 11.1 Create CompilationEngine.psm1 module
    - Implement Invoke-CompilationPass function for pdflatex execution
    - Implement Invoke-BibliographyProcessing function for biber execution
    - Implement Invoke-PdfLatex helper with -interaction=nonstopmode and -file-line-error flags
    - Implement Invoke-Biber helper for bibliography processing
    - Implement Monitor-ProcessOutput to capture stdout/stderr
    - Implement Parse-ExitCode to interpret process exit codes
    - Return CompilationResult with success status, exit code, output, errors, warnings, duration
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 2.1, 2.2, 2.3, 2.4, 2.5, 11.1, 11.2, 11.3, 11.4, 11.5_

  - [ ]* 11.2 Write unit tests for Compilation Engine
    - Test successful pdflatex execution with mocks
    - Test compilation failure handling
    - Test biber execution
    - Test exit code interpretation
    - Test process output capture
    - _Requirements: 1.1, 1.2, 1.3, 2.1, 2.2, 2.3_

- [ ] 12. Implement Main Orchestrator Module
  - [~] 12.1 Create compile.ps1 main script (PARTIALLY COMPLETE - basic workflow exists)
    - ~~Implement Execute-CompilationPipeline to orchestrate three-pass workflow~~ ✅
    - ~~Execute Pass 1 → Biber → Pass 2 → Pass 3 sequence~~ ✅
    - ~~Implement Finalize-Output to copy and rename PDF~~ ✅
    - Implement Invoke-ThesisCompilation function with parameters: -Clean, -Incremental, -ValidateOnly
    - Implement Initialize-Environment to set up paths and load configuration
    - Implement Handle-CompilationError to process and report errors
    - Call Environment Validator before compilation
    - Call Document Parser to validate structure
    - Call Guideline Validator if enabled in config
    - Call Incremental Build Detector if -Incremental flag set
    - Call Error Diagnostics on failure
    - Call File Manager for output handling
    - Use Progress Reporter throughout workflow
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 2.1, 2.2, 2.3, 2.4, 3.1, 3.2, 3.3, 3.4, 3.5, 4.1, 4.2, 4.3, 5.1, 5.2, 5.3, 5.4, 5.5, 7.1, 7.2, 9.1, 9.2, 10.1, 10.2, 10.3, 10.4, 10.5, 11.3_

  - [ ]* 12.2 Write integration tests for Main Orchestrator
    - Test complete compilation workflow with test fixtures
    - Test error recovery on syntax errors
    - Test clean build functionality
    - Test incremental build detection
    - Test validation-only mode
    - _Requirements: 1.1, 1.2, 1.3, 3.1, 7.1, 9.2_

- [ ] 13. Checkpoint - Ensure end-to-end workflow is operational
  - Ensure all tests pass, ask the user if questions arise.

- [x] 14. Add Windows path handling and platform compatibility
  - [x] 14.1 Enhance all modules for Windows compatibility (COMPLETE - already using Windows paths)
    - ~~Update FileManager to use proper path separators~~ ✅
    - ~~Update CompilationEngine to quote paths with spaces~~ ✅
    - ~~Update path resolution to handle drive letters and backslashes~~ ✅
    - ~~Add executable search using $env:PATH with Windows conventions~~ ✅
    - ~~Test with paths containing spaces~~ ✅
    - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5_

  - [ ]* 14.2 Write integration tests for path handling
    - Test paths with spaces
    - Test drive letter handling
    - Test relative path resolution
    - _Requirements: 11.1, 11.2, 11.3, 11.5_

- [ ] 15. Add configuration file loading and command-line parsing
  - [ ] 15.1 Implement configuration management
    - Create Read-Configuration function to load config.json
    - Implement command-line parameter parsing in compile.ps1
    - Add parameter validation and defaults
    - Support environment variable overrides (TEXLIVE_HOME, THESIS_WORKING_DIR, THESIS_OUTPUT_DIR)
    - Merge configuration sources (defaults → config file → env vars → CLI args)
    - _Requirements: 1.1, 1.4, 4.1, 7.1, 7.2_

  - [ ]* 15.2 Write unit tests for configuration loading
    - Test config.json parsing
    - Test environment variable overrides
    - Test CLI argument precedence
    - Test configuration merging
    - _Requirements: 1.1, 1.4_

- [ ] 16. Final integration and polish
  - [ ] 16.1 Complete error message formatting
    - Add line numbers and file paths to all error messages
    - Format error output with color coding
    - Add suggestions for common errors
    - Include guideline references in compliance violations
    - _Requirements: 5.5, 8.1, 8.2, 8.3_

  - [ ] 16.2 Add comprehensive logging
    - Implement verbose mode logging
    - Log all subprocess invocations
    - Log file operations
    - Add timing information for performance analysis
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

  - [ ]* 16.3 Write end-to-end integration tests
    - Test complete workflow with real LaTeX files
    - Test error scenarios (missing files, syntax errors, missing packages)
    - Test clean builds
    - Test incremental builds
    - Test guideline validation
    - _Requirements: 1.1, 1.2, 1.3, 1.5, 2.1, 2.2, 2.3, 2.4, 2.5, 3.1, 3.2, 3.3, 3.4, 3.5, 5.1, 5.2, 5.3, 5.4, 5.5_

- [ ] 17. Final checkpoint - Complete system validation
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Unit tests validate specific examples and edge cases
- Integration tests validate end-to-end workflows
- The implementation uses PowerShell 5.1+ features (classes, modules, cmdlets)
- All modules should export functions using Export-ModuleMember
- Error handling should use try-catch blocks with detailed error messages
- File operations should use Test-Path before accessing files
- Process execution should capture both stdout and stderr
- Path handling must support Windows conventions (backslashes, drive letters, spaces)

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1"] },
    { "id": 1, "tasks": ["2.1", "3.1"] },
    { "id": 2, "tasks": ["2.2", "3.2", "5.1", "6.1"] },
    { "id": 3, "tasks": ["5.2", "6.2", "7.1", "8.1"] },
    { "id": 4, "tasks": ["7.2", "8.2", "10.1"] },
    { "id": 5, "tasks": ["10.2", "11.1"] },
    { "id": 6, "tasks": ["11.2", "12.1"] },
    { "id": 7, "tasks": ["12.2", "14.1"] },
    { "id": 8, "tasks": ["14.2", "15.1"] },
    { "id": 9, "tasks": ["15.2", "16.1", "16.2"] },
    { "id": 10, "tasks": ["16.3"] }
  ]
}
```
