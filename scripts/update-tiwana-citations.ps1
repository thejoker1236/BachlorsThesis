# Simple sequential Tiwana2014 citation updater
# Replaces citations in order as they appear in the files

$ErrorActionPreference = "Stop"

# New page numbers in order (11 total)
# Note: #7 marked as "nicht verifizierbar" - keeping original or using best estimate
$newPages = @(
    "9--10, 13--17",  # 1
    "5--7",           # 2
    "5",              # 3
    "5--6",           # 4
    "7",              # 5
    "5--6",           # 6
    "10",             # 7 (nicht verifizierbar - keeping original)
    "4",              # 8
    "7--8",           # 9
    "7--8",           # 10
    "3--6"            # 11
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
Write-Host "Simple Tiwana2014 Citation Updater" -ForegroundColor Cyan
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
    
    # Find all Tiwana2014 citations in this file
    $pattern = '\[([^\]]+)\]\{Tiwana2014\}'
    $matches = [regex]::Matches($content, $pattern)
    
    if ($matches.Count -eq 0) {
        Write-Host "  No Tiwana2014 citations found" -ForegroundColor Gray
        Write-Host ""
        continue
    }
    
    Write-Host "  Found $($matches.Count) Tiwana2014 citation(s)" -ForegroundColor Yellow
    
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
        $newCitation = "[$newPages_current]{Tiwana2014}"
        
        # Find and replace the first occurrence
        $index = $content.IndexOf($oldCitation)
        if ($index -ge 0) {
            $content = $content.Remove($index, $oldCitation.Length).Insert($index, $newCitation)
            $fileReplacements++
            $currentIndex++
            
            $note = if ($currentIndex -eq 7) { " (nicht verifizierbar - original kept)" } else { "" }
            Write-Host "  ✓ #$currentIndex`: [$oldPages] → [$newPages_current]$note" -ForegroundColor DarkGreen
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
Write-Host "Total citations updated: $currentIndex/11" -ForegroundColor Yellow
Write-Host "Total replacements: $totalReplacements" -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

if ($currentIndex -eq 11) {
    Write-Host "✓ All 11 citations successfully updated!" -ForegroundColor Green
    Write-Host "⚠ Note: Citation #7 marked as 'nicht verifizierbar' - kept as [10]" -ForegroundColor Yellow
} else {
    Write-Host "⚠ Only $currentIndex/11 citations were updated" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Review: git diff Paper/chapters/" -ForegroundColor White
Write-Host "2. Commit: git add -A && git commit -m 'Update all Tiwana2014 citations'" -ForegroundColor White
