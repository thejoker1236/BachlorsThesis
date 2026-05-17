$thesisRepo = "C:\Users\MF\repos\BachlorsThesis"
$projectDir = "C:\Users\MF\iCloudDrive\Uni\Bachlorsproject"
$oneNote    = "C:\Program Files\Microsoft Office\root\Office16\ONENOTE.EXE"

wt `
  new-tab --title "Claude" -d $thesisRepo powershell -NoExit -Command "claude" `; `
  new-tab --title "Thesis-1" -d $thesisRepo `; `
  new-tab --title "Thesis-2" -d $projectDir

Start-Process -FilePath $oneNote

Start-Process -FilePath "kiro" -ArgumentList "`"$thesisRepo`""
