# UEFA Mobile Auto-Processor Scheduler Setup (PowerShell)
# Creates and manages Windows scheduled tasks for automatic processing

param(
    [Parameter(Position=0)]
    [ValidateSet("create", "status", "start", "stop", "delete", "help")]
    [string]$Action = "help"
)

$TaskName = "UEFA_Mobile_Auto_Processor"
$TaskDescription = "Automatically processes mobile UEFA results files every hour"

function Create-ScheduledTask {
    try {
        # Get current directory and Python executable
        $CurrentDir = Get-Location
        $PythonExe = (Get-Command python).Source
        $ScriptPath = Join-Path $CurrentDir "mobile_auto_processor.py"
        
        Write-Host "🔧 Creating scheduled task..." -ForegroundColor Yellow
        Write-Host "   Directory: $CurrentDir" -ForegroundColor Gray
        Write-Host "   Python: $PythonExe" -ForegroundColor Gray
        Write-Host "   Script: $ScriptPath" -ForegroundColor Gray
        
        # Delete existing task if it exists
        try {
            Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
            Write-Host "🗑️ Removed existing task" -ForegroundColor Gray
        } catch {
            # Task didn't exist, that's fine
        }
        
        # Create trigger for every hour
        $HourlyTrigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(5) -RepetitionInterval (New-TimeSpan -Hours 1)
        
        # Create trigger for startup (with delay)
        $StartupTrigger = New-ScheduledTaskTrigger -AtStartup
        $StartupTrigger.Delay = "PT5M"  # 5 minute delay after startup
        
        # Combine triggers
        $Triggers = @($HourlyTrigger, $StartupTrigger)
        
        # Create action
        $Action = New-ScheduledTaskAction -Execute $PythonExe -Argument "`"$ScriptPath`" once" -WorkingDirectory $CurrentDir
        
        # Task settings
        $Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -MultipleInstances IgnoreNew
        
        # Create principal (run as current user)
        $Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive
        
        # Register the task
        Register-ScheduledTask -TaskName $TaskName -Description $TaskDescription -Trigger $Triggers -Action $Action -Settings $Settings -Principal $Principal -Force
        
        Write-Host "✅ Successfully created scheduled task: $TaskName" -ForegroundColor Green
        Write-Host "📅 Task runs every hour and on system startup (5min delay)" -ForegroundColor Green
        Write-Host "🎯 Use 'Get-ScheduledTask -TaskName $TaskName' to verify" -ForegroundColor Cyan
        
        return $true
    }
    catch {
        Write-Host "❌ Failed to create scheduled task: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

function Get-TaskStatus {
    try {
        $Task = Get-ScheduledTask -TaskName $TaskName -ErrorAction Stop
        $TaskInfo = Get-ScheduledTaskInfo -TaskName $TaskName
        
        Write-Host "✅ Scheduled task '$TaskName' exists" -ForegroundColor Green
        Write-Host "📊 State: $($Task.State)" -ForegroundColor Cyan
        Write-Host "📅 Last Run: $($TaskInfo.LastRunTime)" -ForegroundColor Cyan
        Write-Host "⏰ Next Run: $($TaskInfo.NextRunTime)" -ForegroundColor Cyan
        Write-Host "🔄 Last Result: $($TaskInfo.LastTaskResult)" -ForegroundColor Cyan
        
        if ($Task.State -eq "Running") {
            Write-Host "🟢 Task is currently running" -ForegroundColor Green
        } elseif ($Task.State -eq "Ready") {
            Write-Host "🟡 Task is ready and waiting for next trigger" -ForegroundColor Yellow
        } else {
            Write-Host "🔴 Task state: $($Task.State)" -ForegroundColor Red
        }
        
        return $true
    }
    catch {
        Write-Host "❌ Scheduled task '$TaskName' not found" -ForegroundColor Red
        return $false
    }
}

function Start-TaskNow {
    try {
        Start-ScheduledTask -TaskName $TaskName
        Write-Host "✅ Started task '$TaskName'" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "❌ Failed to start task: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

function Stop-TaskNow {
    try {
        Stop-ScheduledTask -TaskName $TaskName
        Write-Host "✅ Stopped task '$TaskName'" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "❌ Failed to stop task: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

function Remove-ScheduledTask {
    try {
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
        Write-Host "✅ Deleted task '$TaskName'" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "❌ Failed to delete task: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

function Show-Help {
    Write-Host "🕰️ UEFA Mobile Auto-Processor Scheduler" -ForegroundColor Cyan
    Write-Host "=" * 50
    Write-Host ""
    Write-Host "This script manages Windows scheduled tasks for automatic UEFA results processing."
    Write-Host ""
    Write-Host "Commands:" -ForegroundColor Yellow
    Write-Host "  create   - Create the scheduled task (runs every hour)" -ForegroundColor White
    Write-Host "  status   - Show current task status and next run time" -ForegroundColor White
    Write-Host "  start    - Start the task immediately" -ForegroundColor White
    Write-Host "  stop     - Stop the running task" -ForegroundColor White
    Write-Host "  delete   - Remove the scheduled task" -ForegroundColor White
    Write-Host "  help     - Show this help message" -ForegroundColor White
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Yellow
    Write-Host "  .\setup_scheduler.ps1 create" -ForegroundColor Gray
    Write-Host "  .\setup_scheduler.ps1 status" -ForegroundColor Gray
    Write-Host "  .\setup_scheduler.ps1 start" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Manual Task Management:" -ForegroundColor Yellow
    Write-Host "  Get-ScheduledTask -TaskName '$TaskName'" -ForegroundColor Gray
    Write-Host "  Start-ScheduledTask -TaskName '$TaskName'" -ForegroundColor Gray
    Write-Host "  Stop-ScheduledTask -TaskName '$TaskName'" -ForegroundColor Gray
}

# Main execution
Write-Host "🕰️ UEFA Mobile Auto-Processor Scheduler" -ForegroundColor Cyan
Write-Host "=" * 50

switch ($Action) {
    "create" {
        if (Create-ScheduledTask) {
            Write-Host ""
            Write-Host "🎉 Setup complete! The auto-processor will run every hour." -ForegroundColor Green
            Write-Host "📱 Enter results on mobile → 🔄 Automatic processing → 📊 Updated rankings" -ForegroundColor Cyan
        }
    }
    "status" {
        Get-TaskStatus
    }
    "start" {
        Start-TaskNow
    }
    "stop" {
        Stop-TaskNow
    }
    "delete" {
        $confirm = Read-Host "❓ Are you sure you want to delete the scheduled task? (y/n)"
        if ($confirm -eq "y") {
            Remove-ScheduledTask
        }
    }
    "help" {
        Show-Help
    }
    default {
        Show-Help
    }
}