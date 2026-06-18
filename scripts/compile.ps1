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
    
    # 3. Clean auxiliary files if requested
    if ($Clean) {
        Write-Log "Step 3: Cleaning auxiliary files (Clean mode)"
        Clear-AuxiliaryFiles
    } else {
        Write-Log "Step 3: Skipping clean (auxiliary files preserved)"
    }
    
    # 4. Check if incremental build can skip
    if ($Incremental) {
        Write-Log "Step 4: Checking incremental build status"
        if (-not (Test-IncrementalBuildNeeded)) {
            Write-Log "Incremental build: No changes detected, skipping compilation" "INFO"
            exit 0
        }
    } else {
        Write-Log "Step 4: Incremental mode not enabled, proceeding with full build"
    }
    
    # 5. Validation only mode
    if ($ValidateOnly) {
        Write-Success "Validation complete (no compilation performed)"
        Write-Log "Validation-only mode: Exiting without compilation" "INFO"
        exit 0
    }
    
    # 6. Change to working directory
    Write-Log "Step 5: Changing to working directory: $paperDir"
    Push-Location $paperDir
    
    # 7. Execute compilation pipeline
    Write-Log "Step 6: Starting compilation pipeline"
    Invoke-CompilationPass -PassNumber 1 -Description "Initial compilation"
    Invoke-BibliographyProcessing
    Invoke-CompilationPass -PassNumber 2 -Description "Integrating references"
    Invoke-CompilationPass -PassNumber 3 -Description "Finalizing cross-references"
    
    # 8. Copy output PDF
    Write-Log "Step 7: Copying output PDF"
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
