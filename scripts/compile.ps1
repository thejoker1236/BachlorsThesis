# Close any Edge window that has main.pdf open (graceful close, not kill)
Get-Process msedge -ErrorAction SilentlyContinue |
    Where-Object { $_.MainWindowTitle -like "*main.pdf*" } |
    ForEach-Object { $_.CloseMainWindow() | Out-Null }

$paperDir = "$PSScriptRoot\..\Paper"

Push-Location $paperDir

try {
    pdflatex -interaction=nonstopmode main.tex
    biber main
    pdflatex -interaction=nonstopmode main.tex
    pdflatex -interaction=nonstopmode main.tex

    # Open compiled PDF in Edge
    Start-Process "msedge" "$paperDir\main.pdf"
}
finally {
    Pop-Location
}
