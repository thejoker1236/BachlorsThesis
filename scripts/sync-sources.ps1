$local  = "$PSScriptRoot\..\sources"
$remote = "C:\Users\MF\iCloudDrive\Uni\Bachlorsproject\sources"
$log    = "$PSScriptRoot\sync-sources.log"

# Newer local files → remote
robocopy $local $remote /E /Z /NP /TEE /XO /LOG:"$log"

# Newer remote files → local
robocopy $remote $local /E /Z /NP /TEE /XO /LOG+:"$log"
