# Monitor CPU usage for specific process
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
    Add-Content -Path "cpu_usage_log.txt" -Value $logMessage
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
    Write-Log "Average CPU Usage: $([math]::Round($avgUsage, 2))%"
    Write-Log "Maximum CPU Usage: $([math]::Round($maxUsage, 2))%"
    Write-Log "Minimum CPU Usage: $([math]::Round($minUsage, 2))%"
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
                    Write-Log "No CPU usage data collected"
                }
                exit
            }
            Write-Log "Waiting for process to start..."
            Start-Sleep -Milliseconds $SampleInterval
            continue
        }
        $lastProcessCheck = $process

        Write-Log "Process found with ID: $($process.Id)"
        # Get CPU usage from Process object
        try {
            $cpuCounter = "\Process($ProcessName)\% Processor Time"
            $counterValue = (Get-Counter $cpuCounter -ErrorAction Stop).CounterSamples.CookedValue
            
            if ($null -ne $counterValue) {
                # Normalize CPU usage by number of logical processors
                $numberOfCores = (Get-WmiObject Win32_ComputerSystem).NumberOfLogicalProcessors
                $cpuUsage = $counterValue / $numberOfCores
                $samples += $cpuUsage
                Write-Log "Current CPU Usage: $([math]::Round($cpuUsage, 2))%"
            } else {
                Write-Log "Failed to get CPU usage value"
            }
        } catch {
            Write-Log "Failed to get CPU counter: $_"
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