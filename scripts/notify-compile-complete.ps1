<#
.SYNOPSIS
    Sends a Windows balloon notification after LaTeX compilation completes.

.PARAMETER Status
    Compilation status: "Success" or "Failed"

.PARAMETER Duration
    Compilation duration in seconds (optional)
#>

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("Success", "Failed")]
    [string]$Status = "Success",
    
    [Parameter(Mandatory=$false)]
    [string]$Duration = "unknown"
)

Add-Type -AssemblyName System.Windows.Forms

try {
    # Create notification icon
    $global:balloon = New-Object System.Windows.Forms.NotifyIcon
    
    # Set icon (use PowerShell icon)
    $path = (Get-Process -id $pid).Path
    $balloon.Icon = [System.Drawing.Icon]::ExtractAssociatedIcon($path)
    
    # Set notification content
    if ($Status -eq "Success") {
        $balloon.BalloonTipIcon = [System.Windows.Forms.ToolTipIcon]::Info
        $balloon.BalloonTipTitle = "Thesis Compilation Complete ✓"
        $balloon.BalloonTipText = "Finished in ${Duration}s at $(Get-Date -Format 'HH:mm:ss')"
    } else {
        $balloon.BalloonTipIcon = [System.Windows.Forms.ToolTipIcon]::Error
        $balloon.BalloonTipTitle = "Thesis Compilation Failed ✗"
        $balloon.BalloonTipText = "Check the output for errors at $(Get-Date -Format 'HH:mm:ss')"
    }
    
    # Show notification
    $balloon.Visible = $true
    $balloon.ShowBalloonTip(5000)
    
    # Keep script running to show notification
    Start-Sleep -Seconds 2
    
    # Clean up
    $balloon.Dispose()
    
} catch {
    Write-Warning "Failed to send notification: $_"
}
