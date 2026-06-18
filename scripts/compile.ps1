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
        return $true
    }
    
    $pdfTime = (Get-Item $pdfPath).LastWriteTime
    $sourceFiles = Get-ChildItem -Path $paperDir -Include *.tex,*.bib -Recurse
    
    foreach ($file in $sourceFiles) {
        if ($file.LastWriteTime -gt $pdfTime) {
            Write-Host "Source modified: $($file.Name)" -ForegroundColor Yellow
            return $true
        }
    }
    
    Write-Success "PDF is up-to-date, skipping compilation"
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
        
        # Extract errors (lines starting with !)
        $content = Get-Content $logFile -Raw
        $errorPattern = '(?m)^!.*?(?=\r?\n\r?\n|\r?\n[^l\s]|\z)'
        $errors = [regex]::Matches($content, $errorPattern)
        
        if ($errors.Count -eq 0) {
            Write-Host "No errors found in log file" -ForegroundColor Gray
            
            # Show warnings instead
            $warnings = Select-String -Path $logFile -Pattern "^LaTeX Warning:" | Select-Object -First 10
            if ($warnings) {
                Write-Host "`n=== Warnings ===" -ForegroundColor Yellow
                foreach ($warn in $warnings) {
                    Write-Host $warn.Line -ForegroundColor DarkYellow
                }
            }
            return
        }
        
        foreach ($error in ($errors | Select-Object -First 10)) {
            $errorText = $error.Value
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
    
    Write-Host "`n╔════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║  LaTeX Thesis Compilation Workflow            ║" -ForegroundColor Cyan
    Write-Host "╚════════════════════════════════════════════════╝" -ForegroundColor Cyan
    
    # 1. Environment Validation
    if (-not (Test-Environment)) {
        exit 1
    }
    
    # 2. Clean auxiliary files if requested
    if ($Clean) {
        Clear-AuxiliaryFiles
    }
    
    # 3. Check if incremental build can skip
    if ($Incremental -and -not (Test-IncrementalBuildNeeded)) {
        exit 0
    }
    
    # 4. Validation only mode
    if ($ValidateOnly) {
        Write-Success "Validation complete"
        exit 0
    }
    
    # 5. Change to working directory
    Push-Location $paperDir
    
    # 6. Execute compilation pipeline
    Invoke-CompilationPass -PassNumber 1 -Description "Initial compilation"
    Invoke-BibliographyProcessing
    Invoke-CompilationPass -PassNumber 2 -Description "Integrating references"
    Invoke-CompilationPass -PassNumber 3 -Description "Finalizing cross-references"
    
    # 7. Copy output PDF
    if (Test-Path $outputPdf) {
        Write-Stage "Copying output PDF"
        Copy-Item $outputPdf "$rootDir\$outputName" -Force
        Write-Success "Copied to: $rootDir\$outputName"
    } else {
        Write-ErrorMsg "Output PDF not found: $outputPdf"
        exit 1
    }
    
    # 8. Success summary
    $duration = (Get-Date) - $startTime
    Write-Host "`n╔════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║  Compilation Successful!                       ║" -ForegroundColor Green
    Write-Host "╚════════════════════════════════════════════════╝" -ForegroundColor Green
    Write-Host "Total time: $($duration.TotalSeconds.ToString('0.0'))s" -ForegroundColor Green
    Write-Host "Output: $outputName`n" -ForegroundColor Green
    
} catch {
    Write-Host "`n╔════════════════════════════════════════════════╗" -ForegroundColor Red
    Write-Host "║  Compilation Failed!                           ║" -ForegroundColor Red
    Write-Host "╚════════════════════════════════════════════════╝" -ForegroundColor Red
    Write-Host "Error: $_`n" -ForegroundColor Red
    exit 1
} finally {
    Pop-Location
}

#endregion
