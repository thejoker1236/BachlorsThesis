$source = "$PSScriptRoot\..\sources"
$destination = "C:\Users\MF\iCloudDrive\Uni\Bachlorsproject\sources"

robocopy $source $destination /MIR /Z /NP /TEE /LOG:"$PSScriptRoot\sync-sources.log"
