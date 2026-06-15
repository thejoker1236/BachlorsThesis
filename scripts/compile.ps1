$paperDir = "$PSScriptRoot\..\Paper"
$rootDir = "$PSScriptRoot\.."
$outputName = "Bachelor-Thesis_Fernando_KI-Monitoring-Systeme.pdf"

Push-Location $paperDir

try {
    pdflatex -interaction=nonstopmode main.tex
    biber main
    pdflatex -interaction=nonstopmode main.tex
    pdflatex -interaction=nonstopmode main.tex

    # Copy compiled PDF to root folder
    if (Test-Path "main.pdf") {
        Copy-Item "main.pdf" "$rootDir\$outputName" -Force
        Write-Host "Copied to: $outputName" -ForegroundColor Green
    }
}
finally {
    Pop-Location
}
