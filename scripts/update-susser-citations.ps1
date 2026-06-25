# Simple sequential Susser2019 citation updater
# Replaces citations in order as they appear in the files

$ErrorActionPreference = "Stop"

# New page numbers in order (16 total)
$newPages = @(
    "27--28, 37",           # 1
    "29, 31--32",           # 2
    "29--32, 38",           # 3
    "26, 31--32",           # 4
    "22, 38--39",           # 5
    "13--17",               # 6
    "3, 14--17",            # 7
    "3, 26--27",            # 8
    "20--21, 38--39",       # 9
    "38",                   # 10
    "10--12, 27--28, 37",   # 11
    "10--12, 28, 44",       # 12
    "37, 43--44",           # 13
    "12, 27, 44",           # 14
    "26--29, 41",           # 15
    "2, 9--12, 28, 37, 43"  # 16
)

# Get chapter files in order
$chaptersPath = "C:\development\PrivProjects\BachlorsThesis\Paper\chapters"
$files = @(
    "01_einleitung.tex",
    "02_grundlagen.tex",
    "03_monitoring_systeme.tex",
    "04_implikationen.tex",
    "05_kritische_betrachtung.tex",
    "06_fazit.tex"
)

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Simple Susser2019 Citation Updater" -ForegroundColor Cyan
Write-Host "Processing files sequentially..." -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

$currentIndex = 0
$totalReplacements = 0

foreach ($filename in $files) {
    $filepath = Join-Path $chaptersPath $filename
    
    if (-not (Test-Path $filepath)) {
        Write-Host "Skipping $filename (not found)" -ForegroundColor Gray
        continue
    }
    
    Write-Host "Processing: $filename" -ForegroundColor Green
    
    $content = Get-Content -Path $filepath -Raw -Encoding UTF8
    $fileReplacements = 0
    
    # Find all Susser2019 citations in this file
    $pattern = '\[([^\]]+)\]\{Susser2019\}'
    $matches = [regex]::Matches($content, $pattern)
    
    if ($matches.Count -eq 0) {
        Write-Host "  No Susser2019 citations found" -ForegroundColor Gray
        Write-Host ""
        continue
    }
    
    Write-Host "  Found $($matches.Count) Susser2019 citation(s)" -ForegroundColor Yellow
    
    # Replace each match with the next new page number
    foreach ($match in $matches) {
        if ($currentIndex -ge $newPages.Count) {
            Write-Host "  ⚠ WARNING: More citations found than expected!" -ForegroundColor Red
            break
        }
        
        $oldPages = $match.Groups[1].Value
        $newPages_current = $newPages[$currentIndex]
        
        # Replace this specific occurrence
        $oldCitation = $match.Value
        $newCitation = "[$newPages_current]{Susser2019}"
        
        # Find and replace the first occurrence
        $index = $content.IndexOf($oldCitation)
        if ($index -ge 0) {
            $content = $content.Remove($index, $oldCitation.Length).Insert($index, $newCitation)
            $fileReplacements++
            $currentIndex++
            
            Write-Host "  ✓ #$currentIndex`: [$oldPages] → [$newPages_current]" -ForegroundColor DarkGreen
        }
    }
    
    # Save the file
    if ($fileReplacements -gt 0) {
        Set-Content -Path $filepath -Value $content -Encoding UTF8 -NoNewline
        $totalReplacements += $fileReplacements
        Write-Host "  → Saved $fileReplacements replacement(s)" -ForegroundColor Cyan
    }
    
    Write-Host ""
}

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Update Complete!" -ForegroundColor Green
Write-Host "Total citations updated: $currentIndex/16" -ForegroundColor Yellow
Write-Host "Total replacements: $totalReplacements" -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

if ($currentIndex -eq 16) {
    Write-Host "✓ All 16 citations successfully updated!" -ForegroundColor Green
} else {
    Write-Host "⚠ Only $currentIndex/16 citations were updated" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Review: git diff Paper/chapters/" -ForegroundColor White
Write-Host "2. Commit: git add -A && git commit -m 'Update all Susser2019 citations'" -ForegroundColor White
Write-Host "3. Clean up: Remove-Item .\scripts\update-susser-citations.ps1" -ForegroundColor White
