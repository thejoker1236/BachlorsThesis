<#
.SYNOPSIS
    Automated LaTeX thesis compilation workflow for FOM Hochschule Bachelor thesis.

.DESCRIPTION
    Orchestrates multi-pass LaTeX compilation (pdflatex → biber → pdflatex → pdflatex),
    validates environment prerequisites, provides error diagnostics, and manages output files.

.PARAMETER Clean
    Remove all auxiliary files (.aux, .bbl, .log, etc.) before compilation.

.PARAMETER Incremental
    Skip compilation if source files haven't changed since last build.

.PARAMETER ValidateOnly
    Validate environment (check for pdflatex, biber) without compiling.

.EXAMPLE
    .\compile.ps1
    Standard compilation with all passes.

.EXAMPLE
    .\compile.ps1 -Clean
    Clean build - remove auxiliary files and recompile.

.EXAMPLE
    .\compile.ps1 -Incremental
    Only compile if sources have changed.

.EXAMPLE
    .\compile.ps1 -ValidateOnly
    Check if LaTeX environment is properly configured.

.NOTES
    Requirements: TeX Live 2026+, pdflatex, biber
    Output: Bachelor-Thesis_Fernando_KI-Monitoring-Systeme.pdf (repository root)
#>

[CmdletBinding()]
param(
    [switch]$Clean,
    [switch]$Incremental,
    [switch]$ValidateOnly
)

$ErrorActionPreference = "Stop"
$paperDir = "$PSScriptRoot\..\Paper"
$rootDir = "$PSScriptRoot\.."
$outputName = "Bachelor-Thesis_Fernando_KI-Monitoring-Systeme.pdf"
$mainDoc = "main.tex"
$outputPdf = "main.pdf"

# Auxiliary file extensions to clean
$auxExtensions = @('.aux', '.bbl', '.bcf', '.blg', '.log', '.out', '.toc', '.lof', '.lot', '.run.xml', '.equ', '.fls', '.fdb_latexmk', '.synctex.gz')

#region Helper Functions

function Write-Stage {
    param([string]$Message, [ConsoleColor]$Color = 'Cyan')
    Write-Host "`n==> $Message" -ForegroundColor $Color
}

function Write-Success {
    param([string]$Message)
    Write-Host "✓ $Message" -ForegroundColor Green
}

function Write-ErrorMsg {
    param([string]$Message)
    Write-Host "✗ $Message" -ForegroundColor Red
}

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    if ($PSCmdlet.MyInvocation.BoundParameters.ContainsKey('Verbose') -or $VerbosePreference -eq 'Continue') {
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        Write-Host "[$timestamp] [$Level] $Message" -ForegroundColor DarkGray
    }
}

function Test-FOMCompliance {
    Write-Stage "Validating FOM Hochschule guidelines compliance"
    Write-Log "Checking document compliance with FOM requirements"
    
    try {
        $mainPath = Join-Path $paperDir $mainDoc
        Write-Log "Main document path: $mainPath"
        
        if (-not (Test-Path $mainPath)) {
            Write-ErrorMsg "Main document not found for validation: $mainPath"
            return $false
        }
        
        $content = Get-Content $mainPath -Raw -ErrorAction Stop
    $violations = @()
    
    # Check 1: Page margins (§5.2.1)
    Write-Log "Checking page margins..."
    if ($content -match '\\usepackage\[([^\]]+)\]\{geometry\}') {
        $geometryOptions = $matches[1]
        
        $expectedMargins = @{
            'left' = '4cm'
            'right' = '2cm'
            'top' = '2.5cm'
            'bottom' = '2cm'
        }
        
        foreach ($margin in $expectedMargins.Keys) {
            if ($geometryOptions -notmatch "$margin=$($expectedMargins[$margin])") {
                $violations += "Margin '$margin' should be $($expectedMargins[$margin]) (FOM §5.2.1)"
            }
        }
        
        if ($violations.Count -eq 0) {
            Write-Log "✓ Page margins are correct"
        }
    } else {
        $violations += "geometry package not found - cannot verify margins (FOM §5.2.1)"
    }
    
    # Check 2: Font settings (§5.2.2)
    Write-Log "Checking font settings..."
    
    # Check for Times New Roman (mathptmx package)
    if ($content -notmatch '\\usepackage\{mathptmx\}') {
        $violations += "Times New Roman font (mathptmx package) not configured (FOM §5.2.2)"
    } else {
        Write-Log "✓ Times New Roman font configured"
    }
    
    # Check for 1.5 line spacing
    if ($content -notmatch '\\onehalfspacing|\\setstretch\{1\.5\}') {
        $violations += "1.5 line spacing not configured (FOM §5.2.2)"
    } else {
        Write-Log "✓ Line spacing 1.5 configured"
    }
    
    # Check 3: Required front matter sections (§5.1)
    Write-Log "Checking required document sections..."
    $requiredSections = @(
        @{Name='Titelblatt'; Pattern='\\maketitle|Titelblatt'},
        @{Name='Inhaltsverzeichnis'; Pattern='\\tableofcontents'},
        @{Name='Abbildungsverzeichnis'; Pattern='\\listoffigures'},
        @{Name='Tabellenverzeichnis'; Pattern='\\listoftables'},
        @{Name='Abkürzungsverzeichnis'; Pattern='\\chapter\*?\{Abkürzungsverzeichnis\}|\\printacronyms'},
        @{Name='Literaturverzeichnis'; Pattern='\\printbibliography|\\bibliography'}
    )
    
    $missingSections = @()
    foreach ($section in $requiredSections) {
        if ($content -notmatch $section.Pattern) {
            $missingSections += $section.Name
        } else {
            Write-Log "✓ Found: $($section.Name)"
        }
    }
    
    if ($missingSections.Count -gt 0) {
        foreach ($missing in $missingSections) {
            $violations += "Missing required section: $missing (FOM §5.1)"
        }
    }
    
    # Report results
    if ($violations.Count -eq 0) {
        Write-Success "Document is compliant with FOM guidelines"
        return $true
    } else {
        Write-Host "`n⚠ FOM Guideline Compliance Issues:" -ForegroundColor Yellow
        foreach ($violation in $violations) {
            Write-Host "  • $violation" -ForegroundColor DarkYellow
        }
        Write-Host ""
        
        # Non-blocking warnings - return true to continue
        Write-Log "FOM compliance check found $($violations.Count) issues (non-blocking)" "WARN"
        return $true
    }
    } catch {
        Write-ErrorMsg "FOM compliance check failed: $_"
        Write-Log "FOM compliance error: $_" "ERROR"
        return $true  # Non-blocking
    }
}

function Test-DocumentStructure {
    Write-Stage "Validating document structure"
    Write-Log "Parsing main document and checking references"
    
    $mainPath = Join-Path $paperDir $mainDoc
    if (-not (Test-Path $mainPath)) {
        Write-ErrorMsg "Main document not found: $mainPath"
        return $false
    }
    
    $content = Get-Content $mainPath -Raw
    $valid = $true
    
    # Check for bibliography file
    if ($content -match '\\addbibresource\{([^}]+)\}') {
        $bibFile = $matches[1]
        $bibPath = Join-Path $paperDir $bibFile
        if (-not (Test-Path $bibPath)) {
            Write-ErrorMsg "Bibliography file not found: $bibFile"
            $valid = $false
        } else {
            Write-Log "Found bibliography: $bibFile"
        }
    }
    
    # Extract chapter includes
    $includes = [regex]::Matches($content, '\\input\{([^}]+)\}|\\include\{([^}]+)\}')
    $missingFiles = @()
    
    foreach ($match in $includes) {
        $file = if ($match.Groups[1].Success) { $match.Groups[1].Value } else { $match.Groups[2].Value }
        
        # Add .tex extension if not present
        if ($file -notmatch '\.tex$') {
            $file += '.tex'
        }
        
        $filePath = Join-Path $paperDir $file
        if (-not (Test-Path $filePath)) {
            $missingFiles += $file
            $valid = $false
        } else {
            Write-Log "Found chapter: $file"
        }
    }
    
    if ($missingFiles.Count -gt 0) {
        Write-ErrorMsg "Missing chapter files:"
        foreach ($file in $missingFiles) {
            Write-Host "  - $file" -ForegroundColor Red
        }
        return $false
    }
    
    Write-Success "Document structure is valid"
    return $true
}

function Test-FOMCompliance {
    Write-Stage "Validating FOM Hochschule guidelines"
    Write-Log "Checking document compliance with FOM requirements"
    
    $mainPath = Join-Path $paperDir $mainDoc
    $content = Get-Content $mainPath -Raw
    $violations = @()
    $warnings = @()
    
    # Check 1: Page geometry (margins)
    if ($content -match '\\usepackage\[([^\]]+)\]\{geometry\}') {
        $geometryArgs = $matches[1]
        Write-Log "Found geometry settings: $geometryArgs"
        
        if ($geometryArgs -match 'left=4cm' -and 
            $geometryArgs -match 'right=2cm' -and 
            $geometryArgs -match 'top=2\.5cm' -and 
            $geometryArgs -match 'bottom=2cm') {
            Write-Log "✓ Margins comply with FOM guidelines"
        } else {
            $violations += "Page margins don't match FOM requirements (left=4cm, right=2cm, top=2.5cm, bottom=2cm)"
        }
    } else {
        $violations += "No geometry package found - cannot verify margins"
    }
    
    # Check 2: Font (Times New Roman via mathptmx)
    if ($content -match '\\usepackage\{mathptmx\}') {
        Write-Log "✓ Times New Roman font configured (mathptmx)"
    } else {
        $violations += "Times New Roman font not configured (missing mathptmx package)"
    }
    
    # Check 3: Line spacing (1.5x)
    if ($content -match '\\usepackage\{setspace\}' -and $content -match '\\onehalfspacing') {
        Write-Log "✓ 1.5x line spacing configured"
    } else {
        $violations += "1.5x line spacing not configured (missing setspace/onehalfspacing)"
    }
    
    # Check 4: Font size (12pt in documentclass)
    if ($content -match '\\documentclass\[([^\]]*12pt[^\]]*)\]') {
        Write-Log "✓ 12pt font size configured"
    } else {
        $violations += "12pt font size not configured in documentclass"
    }
    
    # Check 5: Required sections exist
    $requiredSections = @{
        'Titelblatt' = '(\\maketitle|Titelblatt)'
        'Inhaltsverzeichnis' = '\\tableofcontents'
        'Abbildungsverzeichnis' = '\\listoffigures'
        'Abkürzungsverzeichnis' = '(\\chapter.*Abkürzungsverzeichnis|\\begin\{acronym\})'
        'Literaturverzeichnis' = '(\\printbibliography|\\bibliography)'
    }
    
    foreach ($section in $requiredSections.GetEnumerator()) {
        if ($content -match $section.Value) {
            Write-Log "✓ Found required section: $($section.Key)"
        } else {
            $warnings += "Missing or not detected: $($section.Key)"
        }
    }
    
    # Display results
    if ($violations.Count -eq 0 -and $warnings.Count -eq 0) {
        Write-Success "Document complies with FOM guidelines"
        return $true
    }
    
    if ($violations.Count -gt 0) {
        Write-Host "`n⚠ FOM Guideline Violations:" -ForegroundColor Red
        foreach ($violation in $violations) {
            Write-Host "  ✗ $violation" -ForegroundColor Red
        }
    }
    
    if ($warnings.Count -gt 0) {
        Write-Host "`n⚠ FOM Guideline Warnings:" -ForegroundColor Yellow
        foreach ($warning in $warnings) {
            Write-Host "  ! $warning" -ForegroundColor Yellow
        }
    }
    
    return ($violations.Count -eq 0)
}

function Test-AcronymUsage {
    Write-Stage "Validating acronym usage"
    Write-Log "Checking if all defined acronyms are used and all used acronyms are defined"
    
    $mainPath = Join-Path $paperDir $mainDoc
    $content = Get-Content $mainPath -Raw
    
    # Extract defined acronyms from main.tex
    $definedAcronyms = @{}
    $acronymMatches = [regex]::Matches($content, '\\acro\{([^}]+)\}\{([^}]+)\}')
    
    foreach ($match in $acronymMatches) {
        $shortForm = $match.Groups[1].Value
        $longForm = $match.Groups[2].Value
        $definedAcronyms[$shortForm] = $longForm
        Write-Log "Defined acronym: $shortForm = $longForm"
    }
    
    if ($definedAcronyms.Count -eq 0) {
        Write-Host "  No acronyms defined (skipping usage check)" -ForegroundColor Gray
        return $true
    }
    
    # Collect all text content from chapters
    $allText = $content
    $chapterFiles = Get-ChildItem -Path $paperDir -Filter "chapters/*.tex" -Recurse -ErrorAction SilentlyContinue
    
    foreach ($file in $chapterFiles) {
        $chapterContent = Get-Content $file.FullName -Raw
        $allText += "`n" + $chapterContent
        Write-Log "Scanning chapter: $($file.Name)"
    }
    
    # Find acronym usage (\ac{ACRONYM})
    $usedAcronyms = @{}
    $usageMatches = [regex]::Matches($allText, '\\ac\{([^}]+)\}')
    
    foreach ($match in $usageMatches) {
        $acronym = $match.Groups[1].Value
        if (-not $usedAcronyms.ContainsKey($acronym)) {
            $usedAcronyms[$acronym] = 0
        }
        $usedAcronyms[$acronym]++
    }
    
    Write-Log "Found $($usedAcronyms.Count) unique acronyms used in text"
    
    # Check 1: Undefined acronyms being used
    $undefinedUsed = @()
    foreach ($used in $usedAcronyms.Keys) {
        if (-not $definedAcronyms.ContainsKey($used)) {
            $undefinedUsed += $used
        }
    }
    
    # Check 2: Defined but never used (with printonlyused, these won't appear)
    $definedNotUsed = @()
    foreach ($defined in $definedAcronyms.Keys) {
        if (-not $usedAcronyms.ContainsKey($defined)) {
            $definedNotUsed += $defined
        }
    }
    
    # Report results
    $hasIssues = $false
    
    if ($undefinedUsed.Count -gt 0) {
        Write-Host "`n⚠ Undefined Acronyms Used:" -ForegroundColor Red
        foreach ($acr in $undefinedUsed) {
            Write-Host "  ✗ \ac{$acr} used but not defined (used $($usedAcronyms[$acr]) times)" -ForegroundColor Red
        }
        $hasIssues = $true
    }
    
    if ($definedNotUsed.Count -gt 0) {
        Write-Host "`n⚠ Defined Acronyms Never Used:" -ForegroundColor Yellow
        foreach ($acr in $definedNotUsed) {
            Write-Host "  ! \acro{$acr}{$($definedAcronyms[$acr])} defined but never used" -ForegroundColor Yellow
        }
        Write-Host "  Note: With [printonlyused] option, unused acronyms won't appear in the list" -ForegroundColor DarkGray
    }
    
    if (-not $hasIssues -and $definedNotUsed.Count -eq 0) {
        Write-Success "All acronyms properly defined and used ($($usedAcronyms.Count) acronyms active)"
    } elseif (-not $hasIssues) {
        Write-Success "All used acronyms are properly defined"
    }
    
    return (-not $hasIssues)
}

function Test-Environment {
    Write-Stage "Validating LaTeX environment"
    
    $missing = @()
    
    # Check for pdflatex
    if (-not (Get-Command pdflatex -ErrorAction SilentlyContinue)) {
        $missing += "pdflatex"
    } else {
        Write-Success "pdflatex found"
    }
    
    # Check for biber
    if (-not (Get-Command biber -ErrorAction SilentlyContinue)) {
        $missing += "biber"
    } else {
        Write-Success "biber found"
    }
    
    if ($missing.Count -gt 0) {
        Write-ErrorMsg "Missing executables: $($missing -join ', ')"
        Write-Host "`nInstall with: tlmgr install $($missing -join ' ')" -ForegroundColor Yellow
        return $false
    }
    
    return $true
}

function Clear-AuxiliaryFiles {
    Write-Stage "Cleaning auxiliary files"
    
    $removed = 0
    foreach ($ext in $auxExtensions) {
        $files = Get-ChildItem -Path $paperDir -Filter "*$ext" -ErrorAction SilentlyContinue
        foreach ($file in $files) {
            Remove-Item $file.FullName -Force
            $removed++
        }
    }
    
    Write-Success "Removed $removed auxiliary files"
}

function Test-IncrementalBuildNeeded {
    $pdfPath = Join-Path $rootDir $outputName
    
    if (-not (Test-Path $pdfPath)) {
        Write-Log "Output PDF doesn't exist, full build required"
        return $true
    }
    
    $pdfTime = (Get-Item $pdfPath).LastWriteTime
    Write-Log "Output PDF last modified: $pdfTime"
    
    # Check all source files
    $sourceFiles = Get-ChildItem -Path $paperDir -Include *.tex,*.bib -Recurse -File
    $modifiedFiles = @()
    
    foreach ($file in $sourceFiles) {
        if ($file.LastWriteTime -gt $pdfTime) {
            $modifiedFiles += $file.Name
            Write-Log "Modified: $($file.Name) ($($file.LastWriteTime))"
        }
    }
    
    if ($modifiedFiles.Count -gt 0) {
        Write-Host "Modified files detected:" -ForegroundColor Yellow
        foreach ($file in ($modifiedFiles | Select-Object -First 5)) {
            Write-Host "  • $file" -ForegroundColor Yellow
        }
        if ($modifiedFiles.Count -gt 5) {
            Write-Host "  • ... and $($modifiedFiles.Count - 5) more" -ForegroundColor Yellow
        }
        return $true
    }
    
    # Check if any images changed
    $imageFiles = Get-ChildItem -Path $paperDir -Include *.png,*.jpg,*.pdf,*.eps -Recurse -File -ErrorAction SilentlyContinue
    foreach ($img in $imageFiles) {
        if ($img.LastWriteTime -gt $pdfTime) {
            Write-Host "Image modified: $($img.Name)" -ForegroundColor Yellow
            return $true
        }
    }
    
    Write-Success "PDF is up-to-date (no source changes since $pdfTime)"
    return $false
}

function Invoke-CompilationPass {
    param(
        [int]$PassNumber,
        [string]$Description
    )
    
    Write-Stage "$Description (Pass $PassNumber/3)"
    
    $output = & pdflatex -interaction=nonstopmode -file-line-error $mainDoc 2>&1
    $exitCode = $LASTEXITCODE
    
    # Check if PDF was generated (best indicator of success)
    $pdfExists = Test-Path $outputPdf
    
    # pdflatex returns non-zero for warnings, only fail if PDF wasn't created
    if (-not $pdfExists) {
        Write-ErrorMsg "Compilation failed on pass $PassNumber (no PDF generated)"
        Get-CompilationErrors
        Get-CompilationWarnings
        throw "LaTeX compilation failed on pass $PassNumber"
    }
    
    # Show warnings if exit code was non-zero but PDF exists
    if ($exitCode -ne 0) {
        Write-Host "⚠ Pass completed with warnings (exit code: $exitCode)" -ForegroundColor Yellow
        Get-CompilationWarnings
    } else {
        Write-Success "Pass $PassNumber completed"
    }
}

function Invoke-BibliographyProcessing {
    Write-Stage "Processing bibliography with biber"
    
    $output = & biber main 2>&1
    $exitCode = $LASTEXITCODE
    
    # Check if .bbl file was generated
    $bblExists = Test-Path "main.bbl"
    
    if (-not $bblExists) {
        Write-ErrorMsg "Bibliography processing failed (no .bbl file generated)"
        Get-BibliographyErrors
        throw "Bibliography processing failed"
    }
    
    if ($exitCode -ne 0) {
        Write-Host "⚠ Bibliography processed with warnings" -ForegroundColor Yellow
    } else {
        Write-Success "Bibliography processed"
    }
}

function Get-CompilationWarnings {
    $logFile = Join-Path $paperDir "main.log"
    
    if (Test-Path $logFile) {
        $warnings = Select-String -Path $logFile -Pattern "^LaTeX Warning:|^Package.*Warning:" | Select-Object -First 15
        
        if ($warnings.Count -gt 0) {
            Write-Host "`n=== Compilation Warnings ===" -ForegroundColor Yellow
            foreach ($warn in $warnings) {
                Write-Host $warn.Line -ForegroundColor DarkYellow
            }
            if ($warnings.Count -ge 15) {
                Write-Host "... (showing first 15 warnings)" -ForegroundColor DarkGray
            }
        }
    }
}

function Get-CompilationErrors {
    $logFile = Join-Path $paperDir "main.log"
    
    if (Test-Path $logFile) {
        Write-Host "`n=== Compilation Errors ===" -ForegroundColor Yellow
        
        # Extract errors with file and line info
        $content = Get-Content $logFile -Raw
        
        # Pattern for errors with file:line format (from -file-line-error)
        $fileLineErrors = [regex]::Matches($content, '(?m)^(\.\/[^:]+):(\d+): (.+?)$')
        
        if ($fileLineErrors.Count -gt 0) {
            foreach ($match in ($fileLineErrors | Select-Object -First 15)) {
                $file = $match.Groups[1].Value
                $line = $match.Groups[2].Value
                $msg = $match.Groups[3].Value
                
                Write-Host "${file}:${line}" -ForegroundColor Cyan -NoNewline
                Write-Host " $msg" -ForegroundColor Red
            }
            
            if ($fileLineErrors.Count -gt 15) {
                Write-Host "... and $($fileLineErrors.Count - 15) more errors" -ForegroundColor DarkRed
            }
            return
        }
        
        # Fallback: Extract generic errors (lines starting with !)
        $errorPattern = '(?m)^!.*?(?=\r?\n\r?\n|\r?\n[^l\s]|\z)'
        $errors = [regex]::Matches($content, $errorPattern)
        
        if ($errors.Count -eq 0) {
            Write-Host "No critical errors found in log file" -ForegroundColor Gray
            return
        }
        
        foreach ($error in ($errors | Select-Object -First 10)) {
            $errorText = $error.Value
            
            # Try to extract file and line info from error context
            if ($errorText -match 'l\.(\d+)') {
                $lineNum = $matches[1]
                Write-Host "Line ${lineNum}: " -ForegroundColor Cyan -NoNewline
            }
            
            Write-Host $errorText -ForegroundColor Red
            Write-Host ""
        }
        
        if ($errors.Count -gt 10) {
            Write-Host "... and $($errors.Count - 10) more errors" -ForegroundColor DarkRed
        }
    }
}

function Get-BibliographyErrors {
    $blgFile = Join-Path $paperDir "main.blg"
    
    if (Test-Path $blgFile) {
        Write-Host "`n=== Bibliography Errors ===" -ForegroundColor Yellow
        $errors = Select-String -Path $blgFile -Pattern "(ERROR|WARN)" 
        
        if ($errors.Count -eq 0) {
            Write-Host "No bibliography errors found" -ForegroundColor Gray
            return
        }
        
        foreach ($error in $errors | Select-Object -First 10) {
            if ($error.Line -match "ERROR") {
                Write-Host $error.Line -ForegroundColor Red
            } else {
                Write-Host $error.Line -ForegroundColor DarkYellow
            }
        }
        
        if ($errors.Count -gt 10) {
            Write-Host "... and $($errors.Count - 10) more issues" -ForegroundColor DarkRed
        }
    }
}

#endregion

#region Main Execution

try {
    $startTime = Get-Date
    Write-Log "Starting LaTeX thesis compilation workflow" "INFO"
    
    Write-Host "`n╔════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║  LaTeX Thesis Compilation Workflow            ║" -ForegroundColor Cyan
    Write-Host "╚════════════════════════════════════════════════╝" -ForegroundColor Cyan
    
    # 1. Environment Validation
    Write-Log "Step 1: Environment validation"
    if (-not (Test-Environment)) {
        Write-Log "Environment validation failed" "ERROR"
        exit 1
    }
    
    # 2. Document Structure Validation
    Write-Log "Step 2: Document structure validation"
    if (-not (Test-DocumentStructure)) {
        Write-Log "Document structure validation failed" "ERROR"
        exit 1
    }
    
    # 3. FOM Guideline Compliance Check
    Write-Log "Step 3: FOM guideline compliance check"
    if (-not (Test-FOMCompliance)) {
        Write-Host "`nNote: Compilation will continue despite guideline violations`n" -ForegroundColor Yellow
    }
    
    # 4. Acronym Usage Validation
    Write-Log "Step 4: Acronym usage validation"
    if (-not (Test-AcronymUsage)) {
        Write-Host "`nNote: Compilation will continue despite acronym issues`n" -ForegroundColor Yellow
    }
    
    # 5. Clean auxiliary files if requested
    if ($Clean) {
        Write-Log "Step 5: Cleaning auxiliary files (Clean mode)"
        Clear-AuxiliaryFiles
    } else {
        Write-Log "Step 5: Skipping clean (auxiliary files preserved)"
    }
    
    # 6. Check if incremental build can skip
    if ($Incremental) {
        Write-Log "Step 6: Checking incremental build status"
        if (-not (Test-IncrementalBuildNeeded)) {
            Write-Log "Incremental build: No changes detected, skipping compilation" "INFO"
            exit 0
        }
    } else {
        Write-Log "Step 6: Incremental mode not enabled, proceeding with full build"
    }
    
    # 7. Validation only mode
    if ($ValidateOnly) {
        Write-Success "Validation complete (no compilation performed)"
        Write-Log "Validation-only mode: Exiting without compilation" "INFO"
        exit 0
    }
    
    # 8. Change to working directory
    Write-Log "Step 8: Changing to working directory: $paperDir"
    Push-Location $paperDir
    
    # 9. Execute compilation pipeline
    Write-Log "Step 9: Starting compilation pipeline"
    Invoke-CompilationPass -PassNumber 1 -Description "Initial compilation"
    Invoke-BibliographyProcessing
    Invoke-CompilationPass -PassNumber 2 -Description "Integrating references"
    Invoke-CompilationPass -PassNumber 3 -Description "Finalizing cross-references"
    
    # 10. Copy output PDF
    Write-Log "Step 10: Copying output PDF"
    if (Test-Path $outputPdf) {
        Write-Stage "Copying output PDF"
        Copy-Item $outputPdf "$rootDir\$outputName" -Force
        Write-Success "Copied to: $rootDir\$outputName"
        Write-Log "Output PDF copied successfully to: $rootDir\$outputName"
    } else {
        Write-ErrorMsg "Output PDF not found: $outputPdf"
        Write-Log "Output PDF not found: $outputPdf" "ERROR"
        exit 1
    }
    
    # 9. Success summary
    $duration = (Get-Date) - $startTime
    Write-Log "Compilation completed successfully in $($duration.TotalSeconds) seconds" "INFO"
    
    Write-Host "`n╔════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║  Compilation Successful!                       ║" -ForegroundColor Green
    Write-Host "╚════════════════════════════════════════════════╝" -ForegroundColor Green
    Write-Host "Total time: $($duration.TotalSeconds.ToString('0.0'))s" -ForegroundColor Green
    Write-Host "Output: $outputName`n" -ForegroundColor Green
    
} catch {
    Write-Log "Compilation failed with exception: $_" "ERROR"
    Write-Host "`n╔════════════════════════════════════════════════╗" -ForegroundColor Red
    Write-Host "║  Compilation Failed!                           ║" -ForegroundColor Red
    Write-Host "╚════════════════════════════════════════════════╝" -ForegroundColor Red
    Write-Host "Error: $_`n" -ForegroundColor Red
    exit 1
} finally {
    Pop-Location
    Write-Log "Workflow ended"
}

#endregion
