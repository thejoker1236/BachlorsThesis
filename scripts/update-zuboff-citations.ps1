# Script to update Zuboff2019 citations with correct page numbers
# Based on the complete citation mapping table (32 citations)

$ErrorActionPreference = "Stop"

# Citation replacements in order of appearance (by Zitationsindex)
# Each entry contains: OldPage, NewPage, ApproximateContext for verification
$citationMap = @(
    @{ Nr = 1;  Index = 2;   Old = "69";      New = "14, 16, 195--196"; Context = "Autonomie.*Selbstbestimmung" }
    @{ Nr = 2;  Index = 5;   Old = "69";      New = "14--16";           Context = "strukturelles Merkmal" }
    @{ Nr = 3;  Index = 8;   Old = "69";      New = "244--247";         Context = "Predictive Analytics.*Intelligenz" }
    @{ Nr = 4;  Index = 31;  Old = "69";      New = "67, 222";          Context = "" } # Need to identify context
    @{ Nr = 5;  Index = 36;  Old = "69";      New = "14, 66--68";       Context = "chinesischen.*SCS" }
    @{ Nr = 6;  Index = 92;  Old = "223";     New = "151";              Context = "Rendition" }
    @{ Nr = 7;  Index = 124; Old = "18";      New = "178";              Context = "FBLearner Flow" }
    @{ Nr = 8;  Index = 131; Old = "69";      New = "55--59, 178";      Context = "Verhaltensüberschüssen.*Vorhersageprodukte" }
    @{ Nr = 9;  Index = 132; Old = "28";      New = "265";              Context = "virtuelle Brotkrumen" }
    @{ Nr = 10; Index = 163; Old = "20";      New = "192, 195";         Context = "Emotional Contagion" }
    @{ Nr = 11; Index = 166; Old = "278";     New = "177, 179";         Context = "OCEAN.*Isaak2018" } # First occurrence
    @{ Nr = 12; Index = 168; Old = "278";     New = "177--179";         Context = "OCEAN.*Zuboff2019" } # Second occurrence
    @{ Nr = 13; Index = 175; Old = "69";      New = "14";               Context = "garantierte kommerzielle Ergebnisse" }
    @{ Nr = 14; Index = 181; Old = "69";      New = "14, 133, 222--223"; Context = "" } # Need context
    @{ Nr = 15; Index = 196; Old = "16";      New = "244--247";         Context = "" } # Need context
    @{ Nr = 16; Index = 200; Old = "71";      New = "15, 52, 244--247"; Context = "" } # Need context
    @{ Nr = 17; Index = 207; Old = "69";      New = "14, 55--59";       Context = "Transformation.*Erfahrung|Überwachungskapitalismus beschreibt" }
    @{ Nr = 18; Index = 210; Old = "69\\s*ff\\."; New = "14";           Context = "" }
    @{ Nr = 19; Index = 211; Old = "59";      New = "14, 222--223";     Context = "" }
    @{ Nr = 20; Index = 214; Old = "15";      New = "16, 195--196";     Context = "" }
    @{ Nr = 21; Index = 238; Old = "69";      New = "133, 178, 192--195"; Context = "" }
    @{ Nr = 22; Index = 250; Old = "298";     New = "286, 290";         Context = "Habitualisierung|passive Konsumhaltung" }
    @{ Nr = 23; Index = 259; Old = "283";     New = "176--180, 194--195"; Context = "Verhaltensmuster aktiv formen" }
    @{ Nr = 24; Index = 262; Old = "69";      New = "14, 151";          Context = "" }
    @{ Nr = 25; Index = 263; Old = "69";      New = "55--59, 66--68";   Context = "" }
    @{ Nr = 26; Index = 279; Old = "69";      New = "14, 16, 133, 195"; Context = "" }
    @{ Nr = 27; Index = 283; Old = "69";      New = "14, 55--68";       Context = "" }
    @{ Nr = 28; Index = 284; Old = "62";      New = "14, 133, 178, 222--223"; Context = "instrumentellen Macht|garantierte.*Ergebnisse" }
    @{ Nr = 29; Index = 319; Old = "69";      New = "16, 59--60";       Context = "" }
    @{ Nr = 30; Index = 326; Old = "471";     New = "300--301";         Context = "" }
    @{ Nr = 31; Index = 365; Old = "69";      New = "301--304";         Context = "" }
    @{ Nr = 32; Index = 373; Old = "69";      New = "14--16, 55--68, 178"; Context = "" }
)

# Get all .tex files in the Paper/chapters directory
$chaptersPath = "C:\development\PrivProjects\BachlorsThesis\Paper\chapters"
$texFiles = Get-ChildItem -Path $chaptersPath -Filter "*.tex" | Sort-Object Name

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Zuboff2019 Citation Update Script" -ForegroundColor Cyan
Write-Host "32 citations to update" -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

$totalReplacements = 0
$citationsFound = 0

foreach ($file in $texFiles) {
    Write-Host "Processing: $($file.Name)" -ForegroundColor Green
    
    $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8
    $originalContent = $content
    $fileReplacements = 0
    
    # Process each citation in order
    foreach ($citation in $citationMap) {
        $oldPattern = "\[$($citation.Old)\]\{Zuboff2019\}"
        $newReplacement = "[$($citation.New)]{Zuboff2019}"
        
        # Check if this citation exists in the file
        if ($content -match $oldPattern) {
            $citationsFound++
            
            # If we have context, use it for more precise matching
            if ($citation.Context -and $citation.Context -ne "") {
                $contextPattern = "($($citation.Context).*?)$oldPattern"
                if ($content -match $contextPattern) {
                    $content = $content -replace $contextPattern, "`$1$newReplacement"
                    $fileReplacements++
                    Write-Host "  ✓ #$($citation.Nr) [Index $($citation.Index)]: [$($citation.Old)] → [$($citation.New)]" -ForegroundColor DarkGreen
                    if ($citation.Context) {
                        Write-Host "    Context: $($citation.Context)" -ForegroundColor DarkGray
                    }
                }
                else {
                    # Context didn't match, try without context but warn
                    $matches = [regex]::Matches($content, $oldPattern)
                    if ($matches.Count -eq 1) {
                        # Only one occurrence, safe to replace
                        $content = $content -replace $oldPattern, $newReplacement
                        $fileReplacements++
                        Write-Host "  ⚠ #$($citation.Nr) [Index $($citation.Index)]: [$($citation.Old)] → [$($citation.New)] (no context match)" -ForegroundColor Yellow
                    }
                    else {
                        Write-Host "  ⚠ #$($citation.Nr) [Index $($citation.Index)]: Multiple [$($citation.Old)] found, context required" -ForegroundColor Red
                    }
                }
            }
            else {
                # No context provided, check if it's unique in the file
                $matches = [regex]::Matches($content, $oldPattern)
                if ($matches.Count -eq 1) {
                    $content = $content -replace $oldPattern, $newReplacement
                    $fileReplacements++
                    Write-Host "  ✓ #$($citation.Nr) [Index $($citation.Index)]: [$($citation.Old)] → [$($citation.New)]" -ForegroundColor DarkGreen
                }
                elseif ($matches.Count -gt 1) {
                    Write-Host "  ⚠ #$($citation.Nr) [Index $($citation.Index)]: Multiple [$($citation.Old)] found - need context" -ForegroundColor Red
                }
            }
        }
    }
    
    if ($content -ne $originalContent) {
        # Save the updated content
        Set-Content -Path $file.FullName -Value $content -Encoding UTF8 -NoNewline
        $totalReplacements += $fileReplacements
        Write-Host "  → Saved $fileReplacements replacement(s)" -ForegroundColor Cyan
    } else {
        Write-Host "  No changes needed" -ForegroundColor Gray
    }
    
    Write-Host ""
}

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Update Complete!" -ForegroundColor Green
Write-Host "Citations found: $citationsFound/32" -ForegroundColor Yellow
Write-Host "Total replacements made: $totalReplacements" -ForegroundColor Yellow
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

if ($totalReplacements -lt 32) {
    Write-Host "⚠ WARNING: Not all citations were updated!" -ForegroundColor Red
    Write-Host "Some citations may require manual context identification." -ForegroundColor Magenta
    Write-Host "Review the output above for citations that need attention." -ForegroundColor Magenta
}
else {
    Write-Host "✓ All citations successfully updated!" -ForegroundColor Green
}

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Review the changes with: git diff" -ForegroundColor White
Write-Host "2. Compile the thesis to verify: .\scripts\compile.ps1" -ForegroundColor White
Write-Host "3. Commit the changes: git add -A && git commit -m 'Update Zuboff2019 citations'" -ForegroundColor White

