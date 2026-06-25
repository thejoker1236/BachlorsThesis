# Simple sequential Zuboff2019 citation updater
# Replaces citations in order as they appear in the files

$ErrorActionPreference = "Stop"

# New page numbers in order (32 total)
$newPages = @(
    "14, 16, 195--196",  # 1
    "14--16",            # 2
    "244--247",          # 3
    "67, 222",           # 4
    "14, 66--68",        # 5
    "151",               # 6
    "178",               # 7
    "55--59, 178",       # 8
    "265",               # 9
    "192, 195",          # 10
    "177, 179",          # 11
    "177--179",          # 12
    "14",                # 13
    "14, 133, 222--223", # 14
    "244--247",          # 15
    "15, 52, 244--247",  # 16
    "14, 55--59",        # 17
    "14",                # 18
    "14, 222--223",      # 19
    "16, 195--196",      # 20
    "133, 178, 192--195", # 21
    "286, 290",          # 22
    "176--180, 194--195", # 23
    "14, 151",           # 24
    "55--59, 66--68",    # 25
    "14, 16, 133, 195",  # 26
    "14, 55--68",        # 27
    "14, 133, 178, 222--223", # 28
    "16, 59--60",        # 29
    "300--301",          # 30
    "301--304",          # 31
    "14--16, 55--68, 178" # 32
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
Write-Host "Simple Zuboff2019 Citation Updater" -ForegroundColor Cyan
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
    
    # Find all Zuboff2019 citations in this file
    $pattern = '\[([^\]]+)\]\{Zuboff2019\}'
    $matches = [regex]::Matches($content, $pattern)
    
    Write-Host "  Found $($matches.Count) Zuboff2019 citation(s)" -ForegroundColor Yellow
    
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
        $newCitation = "[$newPages_current]{Zuboff2019}"
        
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
    } else {
        Write-Host "  No changes made" -ForegroundColor Gray
    }
    
    Write-Host ""
}

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Update Complete!" -ForegroundColor Green
Write-Host "Total citations updated: $currentIndex/32" -ForegroundColor Yellow
Write-Host "Total replacements: $totalReplacements" -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

if ($currentIndex -eq 32) {
    Write-Host "✓ All 32 citations successfully updated!" -ForegroundColor Green
} else {
    Write-Host "⚠ Only $currentIndex/32 citations were updated" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Review: git diff Paper/chapters/" -ForegroundColor White
Write-Host "2. Compile: .\scripts\compile.ps1" -ForegroundColor White
Write-Host "3. Commit: git add -A && git commit -m 'Update all Zuboff2019 citations'" -ForegroundColor White
