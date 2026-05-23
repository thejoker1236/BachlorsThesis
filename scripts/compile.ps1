$paperDir = "$PSScriptRoot\..\Paper"

Push-Location $paperDir

try {
    pdflatex -interaction=nonstopmode main.tex
    biber main
    pdflatex -interaction=nonstopmode main.tex
    pdflatex -interaction=nonstopmode main.tex
}
finally {
    Pop-Location
}
