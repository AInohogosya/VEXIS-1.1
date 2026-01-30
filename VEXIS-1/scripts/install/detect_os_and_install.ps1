# Cross-platform dependency detection and installation script for Windows
# Zero-defect policy: comprehensive validation and error handling

param(
    [switch]$Force,
    [switch]$SkipPython,
    [string]$PythonVersion = "3.11"
)

# Logging functions
function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$timestamp] $Message" -ForegroundColor Gray
}

function Write-ErrorLog {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[ERROR] $Message" -ForegroundColor Red
    exit 1
}

function Write-WarningLog {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[WARNING] $Message" -ForegroundColor Yellow
}

function Write-SuccessLog {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[SUCCESS] $Message" -ForegroundColor Green
}

# Detect Windows version and architecture
function Get-SystemInfo {
    Write-Log "Detecting Windows system information..."
    
    $osInfo = Get-CimInstance -ClassName Win32_OperatingSystem
    $arch = $env:PROCESSOR_ARCHITECTURE
    
    Write-Log "Windows detected: $($osInfo.Caption) $($osInfo.Version)"
    Write-Log "Architecture: $arch"
    
    return @{
        OS = "windows"
        Version = $osInfo.Version
        Architecture = $arch
        BuildNumber = $osInfo.BuildNumber
    }
}

# Check if command exists
function Test-Command {
    param([string]$Command)
    try {
        Get-Command $Command -ErrorAction Stop | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

# Check Python installation
function Test-PythonInstallation {
    Write-Log "Checking Python installation..."
    
    $pythonCmd = $null
    $pythonVersion = $null
    
    # Find Python command
    if (Test-Command "python") {
        $pythonCmd = "python"
    }
    elseif (Test-Command "python3") {
        $pythonCmd = "python3"
    }
    elseif (Test-Command "py") {
        $pythonCmd = "py"
    }
    else {
        Write-ErrorLog "Python not found"
    }
    
    # Check version
    try {
        $pythonVersion = & $pythonCmd --version 2>&1
        Write-Log "Found: $pythonVersion"
        
        # Validate version (require 3.8+)
        $versionOutput = & $pythonCmd -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')" 2>&1
        $versionParts = $versionOutput.Split('.')
        $majorVersion = [int]$versionParts[0]
        $minorVersion = [int]$versionParts[1]
        
        if ($majorVersion -lt 3 -or ($majorVersion -eq 3 -and $minorVersion -lt 8)) {
            Write-ErrorLog "Python 3.8 or higher is required. Found: $pythonVersion"
        }
    }
    catch {
        Write-ErrorLog "Failed to validate Python version: $_"
    }
    
    $script:PythonCmd = $pythonCmd
    Write-SuccessLog "Python validation passed: $pythonVersion"
}

# Install Python using winget
function Install-PythonWinget {
    Write-Log "Installing Python using winget..."
    
    if (-not (Test-Command "winget")) {
        Write-ErrorLog "winget not found. Please install Python manually from https://python.org"
    }
    
    try {
        # Install Python
        winget install Python.Python.$PythonVersion --accept-package-agreements --accept-source-agreements
        
        # Refresh PATH
        $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")
        
        # Test installation
        Test-PythonInstallation
    }
    catch {
        Write-ErrorLog "Failed to install Python using winget: $_"
    }
}

# Install Python using chocolatey
function Install-PythonChocolatey {
    Write-Log "Installing Python using Chocolatey..."
    
    if (-not (Test-Command "choco")) {
        Write-ErrorLog "Chocolatey not found. Please install Chocolatey first or use winget."
    }
    
    try {
        # Install Python
        choco install python --yes
        
        # Refresh PATH
        $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")
        
        # Test installation
        Test-PythonInstallation
    }
    catch {
        Write-ErrorLog "Failed to install Python using Chocolatey: $_"
    }
}

# Download and install Python manually
function Install-PythonManual {
    Write-Log "Downloading and installing Python manually..."
    
    $pythonUrl = "https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe"
    $installerPath = "$env:TEMP\python-installer.exe"
    
    try {
        # Download installer
        Write-Log "Downloading Python installer..."
        Invoke-WebRequest -Uri $pythonUrl -OutFile $installerPath
        
        # Install Python
        Write-Log "Installing Python..."
        Start-Process -FilePath $installerPath -ArgumentList "/quiet", "InstallAllUsers=1", "PrependPath=1", "Include_test=0" -Wait
        
        # Clean up
        Remove-Item $installerPath -Force
        
        # Refresh PATH
        $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")
        
        # Test installation
        Test-PythonInstallation
    }
    catch {
        Write-ErrorLog "Failed to install Python manually: $_"
    }
}

# Check and install Python
function Install-Python {
    if ($SkipPython) {
        Write-Log "Skipping Python installation as requested"
        return
    }
    
    if (-not (Test-PythonInstallation) -or $Force) {
        Write-Log "Installing Python..."
        
        # Try winget first
        if (Test-Command "winget") {
            Install-PythonWinget
        }
        # Try chocolatey
        elseif (Test-Command "choco") {
            Install-PythonChocolatey
        }
        # Manual installation
        else {
            Install-PythonManual
        }
    }
}

# Check and install Visual C++ Redistributable
function Install-VcRedist {
    Write-Log "Checking Visual C++ Redistributable..."
    
    # Check if already installed
    $vcRedist = Get-WmiObject -Class Win32_Product | Where-Object { $_.Name -like "*Visual C++*" -and $_.Name -like "*Redistributable*" }
    
    if (-not $vcRedist) {
        Write-Log "Installing Visual C++ Redistributable..."
        
        try {
            $vcRedistUrl = "https://aka.ms/vs/17/release/vc_redist.x64.exe"
            $installerPath = "$env:TEMP\vc_redist.exe"
            
            # Download and install
            Invoke-WebRequest -Uri $vcRedistUrl -OutFile $installerPath
            Start-Process -FilePath $installerPath -ArgumentList "/quiet" -Wait
            Remove-Item $installerPath -Force
            
            Write-SuccessLog "Visual C++ Redistributable installed"
        }
        catch {
            Write-WarningLog "Failed to install Visual C++ Redistributable: $_"
        }
    }
    else {
        Write-Log "Visual C++ Redistributable already installed"
    }
}

# Create and activate virtual environment
function New-VirtualEnvironment {
    Write-Log "Setting up Python virtual environment..."
    
    $venvPath = ".venv"
    
    # Remove existing venv if corrupted
    if (Test-Path $venvPath) {
        try {
            & $script:PythonCmd -c "import sys; sys.path.insert(0, '$venvPath\Lib\site-packages')" 2>$null
        }
        catch {
            Write-Log "Removing corrupted virtual environment..."
            Remove-Item $venvPath -Recurse -Force
        }
    }
    
    # Create virtual environment
    if (-not (Test-Path $venvPath)) {
        Write-Log "Creating virtual environment..."
        & $script:PythonCmd -m venv $venvPath
    }
    
    # Activate and upgrade pip
    Write-Log "Activating virtual environment and upgrading pip..."
    & "$venvPath\Scripts\Activate.ps1"
    python -m pip install --upgrade pip setuptools wheel
    
    Write-SuccessLog "Virtual environment setup complete"
}

# Install Python dependencies
function Install-PythonDependencies {
    Write-Log "Installing Python dependencies..."
    
    # Activate virtual environment
    if (Test-Path ".venv\Scripts\Activate.ps1") {
        & ".venv\Scripts\Activate.ps1"
    }
    
    # Install requirements
    if (Test-Path "requirements.txt") {
        Write-Log "Installing from requirements.txt..."
        pip install -r requirements.txt
    }
    else {
        Write-ErrorLog "requirements.txt not found"
    }
    
    # Install package in development mode
    Write-Log "Installing AI Agent package..."
    pip install -e .
    
    Write-SuccessLog "Python dependencies installed"
}

# Validate installation
function Test-Installation {
    Write-Log "Validating installation..."
    
    # Activate virtual environment
    if (Test-Path ".venv\Scripts\Activate.ps1") {
        & ".venv\Scripts\Activate.ps1"
    }
    
    # Test imports
    Write-Log "Testing core imports..."
    $testScript = @"
import sys
modules = [
    'PIL', 'cv2', 'numpy', 'requests', 'pyautogui', 
    'openai', 'anthropic', 'transformers', 'torch'
]
failed = []
for module in modules:
    try:
        __import__(module)
        print(f'✓ {module}')
    except ImportError as e:
        failed.append(f'{module}: {e}')
        print(f'✗ {module}: {e}')

if failed:
    print(f'\\nFailed imports: {len(failed)}')
    for fail in failed:
        print(f'  - {fail}')
    sys.exit(1)
else:
    print('\\nAll imports successful')
"@
    
    & $script:PythonCmd -c $testScript
    if ($LASTEXITCODE -ne 0) {
        Write-ErrorLog "Import validation failed"
    }
    
    # Test CLI commands
    Write-Log "Testing CLI commands..."
    if (Test-Command "ai-agent") {
        Write-Log "✓ ai-agent command available"
    }
    else {
        Write-ErrorLog "ai-agent command not found"
    }
    
    Write-SuccessLog "Installation validation complete"
}

# Main installation function
function Main {
    Write-Log "Starting AI Agent installation on Windows..."
    Write-Log "Zero-defect policy: comprehensive validation enabled"
    
    # Change to script directory
    Set-Location $PSScriptRoot\..\..
    
    # Get system information
    $systemInfo = Get-SystemInfo
    
    # Install Python
    Install-Python
    
    # Install Visual C++ Redistributable
    Install-VcRedist
    
    # Setup virtual environment
    New-VirtualEnvironment
    
    # Install Python dependencies
    Install-PythonDependencies
    
    # Validate installation
    Test-Installation
    
    Write-SuccessLog "AI Agent installation completed successfully!"
    Write-Log "To activate the environment: .venv\Scripts\Activate.ps1"
    Write-Log "To run the agent: ai-agent --help"
}

# Run main function
Main
