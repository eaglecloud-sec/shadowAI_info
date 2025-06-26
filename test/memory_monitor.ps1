# Monitor memory usage for specific process
param(
    [string]$ProcessName = "OcrLiteNcnn",
    # [string]$ProcessName = "RapidOcrNcnnOld",
    # [string]$ProcessName = "RapidOcrNcnnNew",
    # [string]$ProcessName = "ocr_test_executable",
    [int]$SampleInterval = 100
)

function Get-TimeStamp {
    return "[{0:MM/dd/yyyy} {0:HH:mm:ss}]" -f (Get-Date)
}

function Write-Log {
    param($Message)
    $logMessage = "$(Get-TimeStamp) $Message"
    Write-Host $logMessage
    Add-Content -Path "memory_usage_log.txt" -Value $logMessage
}

function Get-MemoryUsage {
    param($Process)
    # Working Set (物理内存)
    $workingSetMB = [math]::Round($Process.WorkingSet64 / 1MB, 2)
    # Private Working Set (私有内存)
    $privateWorkingSetMB = [math]::Round($Process.PrivateMemorySize64 / 1MB, 2)
    # Peak Working Set
    $peakWorkingSetMB = [math]::Round($Process.PeakWorkingSet64 / 1MB, 2)
    # Page File Usage
    $pageFileMB = [math]::Round($Process.PagedMemorySize64 / 1MB, 2)

    return @{
        WorkingSet = $workingSetMB
        PrivateWorkingSet = $privateWorkingSetMB
        PeakWorkingSet = $peakWorkingSetMB
        PageFile = $pageFileMB
    }
}

function Write-Summary {
    param(
        [DateTime]$startTime,
        [array]$workingSetSamples,
        [array]$privateWorkingSetSamples,
        [array]$pageFileSamples
    )
    $endTime = Get-Date
    $duration = ($endTime - $startTime).TotalSeconds

    function Get-Stats {
        param([array]$samples)
        $avg = ($samples | Measure-Object -Average).Average
        $max = ($samples | Measure-Object -Maximum).Maximum
        $min = ($samples | Measure-Object -Minimum).Minimum
        return @{
            Average = [math]::Round($avg, 2)
            Maximum = [math]::Round($max, 2)
            Minimum = [math]::Round($min, 2)
        }
    }

    $wsStats = Get-Stats $workingSetSamples
    $pwsStats = Get-Stats $privateWorkingSetSamples
    $pfStats = Get-Stats $pageFileSamples

    Write-Log "Monitoring Results:"
    Write-Log "Duration: $([math]::Round($duration, 2)) seconds"
    Write-Log "Working Set (Physical Memory):"
    Write-Log "  Average: $($wsStats.Average) MB"
    Write-Log "  Maximum: $($wsStats.Maximum) MB"
    Write-Log "  Minimum: $($wsStats.Minimum) MB"
    Write-Log "Private Working Set:"
    Write-Log "  Average: $($pwsStats.Average) MB"
    Write-Log "  Maximum: $($pwsStats.Maximum) MB"
    Write-Log "  Minimum: $($pwsStats.Minimum) MB"
    Write-Log "Page File Usage:"
    Write-Log "  Average: $($pfStats.Average) MB"
    Write-Log "  Maximum: $($pfStats.Maximum) MB"
    Write-Log "  Minimum: $($pfStats.Minimum) MB"
    Write-Log "Total Samples: $($workingSetSamples.Count)"
}

# Initialize variables
$workingSetSamples = @()
$privateWorkingSetSamples = @()
$pageFileSamples = @()
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
                if ($workingSetSamples.Count -gt 0) {
                    Write-Summary -startTime $startTime `
                                -workingSetSamples $workingSetSamples `
                                -privateWorkingSetSamples $privateWorkingSetSamples `
                                -pageFileSamples $pageFileSamples
                } else {
                    Write-Log "No memory usage data collected"
                }
                exit
            }
            Write-Log "Waiting for process to start..."
            Start-Sleep -Milliseconds $SampleInterval
            continue
        }
        $lastProcessCheck = $process

        # Get memory usage
        $memoryInfo = Get-MemoryUsage -Process $process
        
        # Store samples
        $workingSetSamples += $memoryInfo.WorkingSet
        $privateWorkingSetSamples += $memoryInfo.PrivateWorkingSet
        $pageFileSamples += $memoryInfo.PageFile

        Write-Log "Memory Usage:"
        Write-Log "  Working Set: $($memoryInfo.WorkingSet) MB"
        Write-Log "  Private Working Set: $($memoryInfo.PrivateWorkingSet) MB"
        Write-Log "  Peak Working Set: $($memoryInfo.PeakWorkingSet) MB"
        Write-Log "  Page File: $($memoryInfo.PageFile) MB"
        
        Start-Sleep -Milliseconds $SampleInterval
    }
}
catch {
    Write-Log "Error occurred: $_"
}
finally {
    if ($workingSetSamples.Count -gt 0) {
        Write-Summary -startTime $startTime `
                    -workingSetSamples $workingSetSamples `
                    -privateWorkingSetSamples $privateWorkingSetSamples `
                    -pageFileSamples $pageFileSamples
    }
}
