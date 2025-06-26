# Monitor GPU usage for specific process
param(
    [string]$ProcessName = "OcrLiteNcnn",
    [int]$SampleInterval = 100
)

function Get-TimeStamp {
    return "[{0:MM/dd/yyyy} {0:HH:mm:ss}]" -f (Get-Date)
}

function Write-Log {
    param($Message)
    $logMessage = "$(Get-TimeStamp) $Message"
    Write-Host $logMessage
    Add-Content -Path "gpu_usage_log.txt" -Value $logMessage
}

function Write-Summary {
    param(
        [DateTime]$startTime,
        [array]$samples
    )
    $endTime = Get-Date
    $duration = ($endTime - $startTime).TotalSeconds
    $avgUsage = ($samples | Measure-Object -Average).Average
    $maxUsage = ($samples | Measure-Object -Maximum).Maximum
    $minUsage = ($samples | Measure-Object -Minimum).Minimum

    Write-Log "Monitoring Results:"
    Write-Log "Duration: $([math]::Round($duration, 2)) seconds"
    Write-Log "Average GPU Usage: $([math]::Round($avgUsage, 2))%"
    Write-Log "Maximum GPU Usage: $([math]::Round($maxUsage, 2))%"
    Write-Log "Minimum GPU Usage: $([math]::Round($minUsage, 2))%"
    Write-Log "Total Samples: $($samples.Count)"
}

# Initialize variables
$samples = @()
$startTime = Get-Date
$lastProcessCheck = $null

Write-Log "Starting monitoring process: $ProcessName"
Write-Log "Sample interval: $SampleInterval ms"

try {
    while ($true) {
        $process = Get-Process $ProcessName -ErrorAction SilentlyContinue
        
        # Check if process exists
        if (-not $process) {
            if ($lastProcessCheck) {
                Write-Log "Process terminated, generating final report..."
                if ($samples.Count -gt 0) {
                    Write-Summary -startTime $startTime -samples $samples
                } else {
                    Write-Log "No GPU usage data collected"
                }
                exit
            }
            Write-Log "Waiting for process to start..."
            Start-Sleep -Milliseconds $SampleInterval
            continue
        }
        $lastProcessCheck = $process

        Write-Log "Process found with ID: $($process.Id)"
        # Get GPU usage from Performance Counter
        $gpuCounter = Get-Counter "\GPU Engine(*)\Utilization Percentage" -ErrorAction SilentlyContinue
        if ($gpuCounter) {
            # Match by process ID
            $gpuUsage = ($gpuCounter.CounterSamples | Where-Object { 
                $_.InstanceName -match "pid_$($process.Id)" -and 
                $_.InstanceName -match "engtype_3d"
            } | Measure-Object -Property CookedValue -Average).Average
            
            if ($gpuUsage) {
                $samples += $gpuUsage
                Write-Log "Current GPU Usage (3D Engine): $([math]::Round($gpuUsage, 2))%"
            } else {
                # Try other engine types
                $allEngineUsage = $gpuCounter.CounterSamples | Where-Object { 
                    $_.InstanceName -match "pid_$($process.Id)" 
                } | ForEach-Object {
                    Write-Log "Found engine usage: $($_.InstanceName)"
                    $_.CookedValue
                } | Measure-Object -Average
                
                if ($allEngineUsage.Count -gt 0) {
                    $samples += $allEngineUsage.Average
                    Write-Log "Current GPU Usage (All Engines): $([math]::Round($allEngineUsage.Average, 2))%"
                } else {
                    Write-Log "No GPU usage data found for any engine type"
                }
            }
        } else {
            Write-Log "Failed to get GPU counter"
        }
        Start-Sleep -Milliseconds $SampleInterval
    }
}
catch {
    Write-Log "Error occurred: $_"
}
finally {
    if ($samples.Count -gt 0) {
        Write-Summary -startTime $startTime -samples $samples
    }
}