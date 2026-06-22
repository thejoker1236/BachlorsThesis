# ============================================================================
# Quellen-Überprüfungsskript für Bachelor-Thesis
# ============================================================================

$ErrorActionPreference = "Continue"
$bibFile = "c:\development\PrivProjects\BachlorsThesis\Paper\references.bib"
$sourcesDir = "c:\development\PrivProjects\BachlorsThesis\sources"
$outputFile = "c:\development\PrivProjects\BachlorsThesis\Quellenprüfung-Bericht.md"

Write-Host "=== Quellen-Überprüfung ===" -ForegroundColor Cyan
Write-Host ""

# ============================================================================
# 1. Vollständigkeitscheck
# ============================================================================
Write-Host "1. Vollständigkeitscheck..." -ForegroundColor Yellow

# BibTeX-Einträge parsen
$bibContent = Get-Content $bibFile -Raw -Encoding UTF8
$bibEntries = @{}
$currentKey = $null

# Einfacher Parser für BibTeX-Keys
$bibContent -split "`n" | ForEach-Object {
    if ($_ -match '@\w+\{([^,]+),') {
        $currentKey = $Matches[1]
        $bibEntries[$currentKey] = @{
            Key = $currentKey
            Found = $false
            PossibleMatches = @()
        }
    }
}

Write-Host "  Gefunden: $($bibEntries.Count) Einträge in references.bib" -ForegroundColor Gray

# PDFs im sources-Verzeichnis finden
$allPdfs = Get-ChildItem -Path $sourcesDir -Filter "*.pdf" -Recurse
Write-Host "  Gefunden: $($allPdfs.Count) PDF-Dateien im sources-Verzeichnis" -ForegroundColor Gray

# Zuordnung: BibKey -> PDF
foreach ($key in $bibEntries.Keys) {
    $entry = $bibEntries[$key]
    
    # Versuche Zuordnung basierend auf Autorennamen oder Schlüsselwörtern
    $searchPatterns = @(
        "*$key*",
        "*$($key -replace '\d+', '')*"  # Key ohne Jahr
    )
    
    foreach ($pattern in $searchPatterns) {
        $matches = $allPdfs | Where-Object { $_.Name -like $pattern }
        if ($matches) {
            $entry.Found = $true
            $entry.PossibleMatches += $matches.Name
            break
        }
    }
}

$missingPdfs = $bibEntries.Values | Where-Object { -not $_.Found }
$foundPdfs = $bibEntries.Values | Where-Object { $_.Found }

Write-Host ""
Write-Host "  ✓ Zugeordnet: $($foundPdfs.Count) / $($bibEntries.Count)" -ForegroundColor Green
Write-Host "  ✗ Nicht gefunden: $($missingPdfs.Count) / $($bibEntries.Count)" -ForegroundColor Red

# ============================================================================
# 2. Konsistenzcheck
# ============================================================================
Write-Host ""
Write-Host "2. Konsistenzcheck..." -ForegroundColor Yellow

# PDFs ohne BibTeX-Eintrag
$unmatchedPdfs = @()
foreach ($pdf in $allPdfs) {
    $matched = $false
    foreach ($key in $bibEntries.Keys) {
        if ($pdf.Name -like "*$key*") {
            $matched = $true
            break
        }
    }
    if (-not $matched) {
        $unmatchedPdfs += $pdf.Name
    }
}

Write-Host "  PDFs ohne BibTeX-Eintrag: $($unmatchedPdfs.Count)" -ForegroundColor Gray

# ============================================================================
# 3. Qualitätscheck (Dateigröße als Proxy)
# ============================================================================
Write-Host ""
Write-Host "3. Qualitätscheck (Dateigröße)..." -ForegroundColor Yellow

$suspiciousFiles = $allPdfs | Where-Object { $_.Length -lt 50KB }
Write-Host "  Verdächtig kleine Dateien (<50KB): $($suspiciousFiles.Count)" -ForegroundColor $(if($suspiciousFiles.Count -gt 0){"Red"}else{"Green"})

$largeFiles = $allPdfs | Where-Object { $_.Length -gt 50MB }
Write-Host "  Sehr große Dateien (>50MB): $($largeFiles.Count)" -ForegroundColor Gray

# ============================================================================
# 4. Nutzungscheck (in LaTeX-Dateien)
# ============================================================================
Write-Host ""
Write-Host "4. Nutzungscheck..." -ForegroundColor Yellow

$texFiles = Get-ChildItem -Path "c:\development\PrivProjects\BachlorsThesis\Paper\chapters" -Filter "*.tex"
$citedKeys = @{}

foreach ($tex in $texFiles) {
    $content = Get-Content $tex.FullName -Raw -Encoding UTF8
    foreach ($key in $bibEntries.Keys) {
        if ($content -match "\\cite\{$key\}|\\footcite\{$key\}|vglfootcite.*?\{$key\}") {
            $citedKeys[$key] = $true
        }
    }
}

$uncitedEntries = $bibEntries.Keys | Where-Object { -not $citedKeys.ContainsKey($_) }

Write-Host "  Zitiert: $($citedKeys.Count) / $($bibEntries.Count)" -ForegroundColor Green
Write-Host "  Nicht zitiert: $($uncitedEntries.Count) / $($bibEntries.Count)" -ForegroundColor Yellow

# ============================================================================
# 5. Metadatencheck (aus BibTeX)
# ============================================================================
Write-Host ""
Write-Host "5. Metadatencheck..." -ForegroundColor Yellow

$entriesWithDOI = ($bibContent -split "`n" | Select-String "doi\s*=" | Measure-Object).Count
$entriesWithURL = ($bibContent -split "`n" | Select-String "url\s*=" | Measure-Object).Count
$entriesWithPages = ($bibContent -split "`n" | Select-String "pages\s*=" | Measure-Object).Count

Write-Host "  Einträge mit DOI: $entriesWithDOI" -ForegroundColor Gray
Write-Host "  Einträge mit URL: $entriesWithURL" -ForegroundColor Gray
Write-Host "  Einträge mit Seitenangaben: $entriesWithPages" -ForegroundColor Gray

# ============================================================================
# Bericht erstellen
# ============================================================================
Write-Host ""
Write-Host "Erstelle Bericht..." -ForegroundColor Cyan

$report = @"
# Quellenprüfung - Bachelor-Thesis
**Datum:** $(Get-Date -Format "dd.MM.yyyy HH:mm")

---

## 1. Vollständigkeitscheck

**Zusammenfassung:**
- BibTeX-Einträge: **$($bibEntries.Count)**
- PDF-Dateien gefunden: **$($allPdfs.Count)**
- Zugeordnet: **$($foundPdfs.Count)** ✓
- Nicht zugeordnet: **$($missingPdfs.Count)** ✗

### Fehlende PDFs (nicht gefunden):

$(if ($missingPdfs.Count -gt 0) {
    $missingPdfs | ForEach-Object { "- **$($_.Key)**`n" }
} else {
    "🎉 Alle BibTeX-Einträge haben zugeordnete PDFs!`n"
})

---

## 2. Konsistenzcheck

**PDFs ohne BibTeX-Eintrag:** $($unmatchedPdfs.Count)

$(if ($unmatchedPdfs.Count -gt 0) {
    "### Nicht zugeordnete PDFs:`n`n"
    $unmatchedPdfs | ForEach-Object { "- $_`n" }
} else {
    "✓ Alle PDFs haben einen entsprechenden BibTeX-Eintrag.`n"
})

---

## 3. Qualitätscheck

### Verdächtig kleine Dateien (<50KB):

$(if ($suspiciousFiles.Count -gt 0) {
    $suspiciousFiles | ForEach-Object { "- **$($_.Name)** ($([math]::Round($_.Length/1KB, 2)) KB)`n" }
} else {
    "✓ Keine verdächtig kleinen Dateien gefunden.`n"
})

### Sehr große Dateien (>50MB):

$(if ($largeFiles.Count -gt 0) {
    $largeFiles | ForEach-Object { "- $($_.Name) ($([math]::Round($_.Length/1MB, 2)) MB)`n" }
} else {
    "✓ Keine ungewöhnlich großen Dateien.`n"
})

---

## 4. Nutzungscheck

**Zitierte Quellen:** $($citedKeys.Count) / $($bibEntries.Count)  
**Nicht zitierte Quellen:** $($uncitedEntries.Count)

### Nicht zitierte BibTeX-Einträge:

$(if ($uncitedEntries.Count -gt 0) {
    $uncitedEntries | ForEach-Object { "- ``$_```n" }
} else {
    "✓ Alle BibTeX-Einträge werden in der Arbeit zitiert!`n"
})

---

## 5. Metadatencheck

**Statistik:**
- Einträge mit DOI: **$entriesWithDOI**
- Einträge mit URL: **$entriesWithURL**
- Einträge mit Seitenangaben: **$entriesWithPages**

**Empfehlung:** Für wissenschaftliche Arbeiten sollten möglichst alle Einträge DOIs oder präzise Seitenangaben enthalten.

---

## Zusammenfassung

| Prüfung | Status | Details |
|---------|--------|---------|
| Vollständigkeit | $(if($missingPdfs.Count -eq 0){"✅"}else{"⚠️"}) | $($foundPdfs.Count)/$($bibEntries.Count) zugeordnet |
| Konsistenz | $(if($unmatchedPdfs.Count -eq 0){"✅"}else{"ℹ️"}) | $($unmatchedPdfs.Count) PDFs ohne Eintrag |
| Qualität | $(if($suspiciousFiles.Count -eq 0){"✅"}else{"⚠️"}) | $($suspiciousFiles.Count) verdächtige Dateien |
| Nutzung | $(if($uncitedEntries.Count -eq 0){"✅"}else{"ℹ️"}) | $($uncitedEntries.Count) ungenutzte Einträge |
| Metadaten | ℹ️ | $entriesWithDOI DOIs vorhanden |

---

**Generiert mit:** ``check-sources.ps1``
"@

$report | Out-File -FilePath $outputFile -Encoding UTF8
Write-Host "✓ Bericht erstellt: $outputFile" -ForegroundColor Green
Write-Host ""
