# Close any Edge window that has main.pdf open (graceful close, not kill)
Get-Process msedge -ErrorAction SilentlyContinue |
    Where-Object { $_.MainWindowTitle -like "*main.pdf*" } |
    ForEach-Object { $_.CloseMainWindow() | Out-Null }

Push-Location $PSScriptRoot

pdflatex main.tex
biber main
pdflatex main.tex
pdflatex main.tex

Pop-Location

# Open compiled PDF in Edge
Start-Process "msedge" "$PSScriptRoot\main.pdf"