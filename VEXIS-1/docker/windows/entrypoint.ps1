# AI Agent Windows Docker Entrypoint
# Zero-defect policy: robust Windows container initialization with proper setup

param(
    [switch]$SkipValidation,
    [switch]$SkipXvfb,
    [string]$LogPath = "C:\app\logs",
    [string]$ConfigPath = "C:\app\config.yaml"
)

# Logging function
function Write-Log {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$timestamp] $Message" -ForegroundColor Gray
}

# Error handling function
function Write-Error {
    param([string]$Message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$timestamp] ERROR: $Message" -ForegroundColor Red
    exit 1
}

# Function to validate environment
function Test-Environment {
    Write-Log "Validating environment..."
    
    # Check Python
    try {
        $pythonVersion = python --version 2>&1
        Write-Log "Python version: $pythonVersion"
    }
    catch {
        Write-Error "Python not found or not accessible"
    }
    
    # Check virtual environment
    if (-not (Test-Path "C:\app\.venv")) {
        Write-Error "Virtual environment not found at C:\app\.venv"
    }
    
    # Check AI Agent installation
    try {
        C:\app\.venv\Scripts\python -c "import ai_agent" 2>$null
        Write-Log "AI Agent installation verified"
    }
    catch {
        Write-Error "AI Agent not properly installed"
    }
    
    Write-Log "Environment validation passed"
}

# Function to setup configuration
function Initialize-Configuration {
    Write-Log "Setting up configuration..."
    
    # Create default config if not exists
    if (-not (Test-Path $ConfigPath)) {
        Write-Log "Creating default configuration..."
        
        $configContent = @"
logging:
  level: INFO
  console: true
  file: C:\app\logs\ai_agent.log
  json_format: false

api:
  timeout: 30
  max_retries: 3
  retry_delay: 1.0
  model: gpt-4-vision-preview

gui:
  click_delay: 0.1
  typing_delay: 0.05
  scroll_duration: 0.5
  drag_duration: 0.3
  screenshot_quality: 95
  screenshot_format: PNG
  coordinate_validation: true

security:
  max_coordinate_value: 1.0
  min_coordinate_value: 0.0
  allowed_commands:
    - click
    - double_click
    - right_click
    - text
    - key
    - drag
    - scroll
    - end
  sanitize_text_input: true
  validate_file_paths: true
  max_text_length: 1000

performance:
  max_concurrent_tasks: 1
  task_timeout: 300
  screenshot_timeout: 10
  api_timeout: 30
  memory_limit_mb: 1024
"@
        
        $configContent | Out-File -FilePath $ConfigPath -Encoding UTF8
        Write-Log "Default configuration created at $ConfigPath"
    }
    
    # Ensure log directory exists
    if (-not (Test-Path $LogPath)) {
        New-Item -ItemType Directory -Path $LogPath -Force | Out-Null
        Write-Log "Created log directory: $LogPath"
    }
    
    # Ensure screenshots directory exists
    $screenshotsPath = "C:\app\screenshots"
    if (-not (Test-Path $screenshotsPath)) {
        New-Item -ItemType Directory -Path $screenshotsPath -Force | Out-Null
        Write-Log "Created screenshots directory: $screenshotsPath"
    }
    
    Write-Log "Configuration setup completed"
}

# Function to run health checks
function Test-Health {
    Write-Log "Running health checks..."
    
    try {
        # Check Python modules
        $healthCheckScript = @"
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
    print(f'\nFailed imports: {len(failed)}')
    for fail in failed:
        print(f'  - {fail}')
    sys.exit(1)
else:
    print('\nAll imports successful')
"@
        
        C:\app\.venv\Scripts\python -c $healthCheckScript
        Write-Log "Python modules health check passed"
        
        # Check AI Agent functionality
        $functionalityCheckScript = @"
from ai_agent.platform_abstraction.platform_detector import get_system_info
from ai_agent.utils.config import load_config

try:
    system_info = get_system_info()
    config = load_config()
    print(f'✓ Platform detection: {system_info.os_name}')
    print(f'✓ Configuration loaded')
    print(f'✓ AI Agent ready')
except Exception as e:
    print(f'✗ Health check failed: {e}')
    sys.exit(1)
"@
        
        C:\app\.venv\Scripts\python -c $functionalityCheckScript
        Write-Log "AI Agent functionality health check passed"
        
    }
    catch {
        Write-Error "Health checks failed: $($_.Exception.Message)"
    }
    
    Write-Log "Health checks completed"
}

# Function to display usage information
function Show-Usage {
    $usageText = @"
AI Agent Windows Docker Container
=================================

Usage Examples:
  # Show help
  docker run -it ai-agent-windows --help
  
  # Run with instruction
  docker run -it --rm -v C:\Users\Public\screenshots:C:\app\screenshots ai-agent-windows `
    "Open a web browser and search for AI"
  
  # Run enhanced mode with session persistence
  docker run -it --rm -v C:\Users\Public\sessions:C:\app\sessions ai-agent-windows `
    python -m ai_agent.enhanced "Automate login process" --session-file C:\app\sessions\login.json
  
  # Run with custom configuration
  docker run -it --rm -v C:\Users\Public\config.yaml:C:\app\config.yaml ai-agent-windows `
    "Click the button at coordinates (0.5, 0.3)"
  
  # Run tests
  docker run -it --rm ai-agent-windows python -m pytest tests/

Environment Variables:
  - AI_AGENT_LOG_LEVEL: Logging level (default: INFO)
  - AI_AGENT_CONFIG_PATH: Path to config file
  - SkipValidation: Skip environment validation
  - SkipXvfb: Skip Xvfb setup (Windows typically doesn't need it)

Mount Points:
  - C:\app\screenshots: Screenshot output directory
  - C:\app\logs: Log files directory
  - C:\app\sessions: Session persistence directory
  - C:\app\config.yaml: Custom configuration file

Windows-Specific Notes:
  - GUI automation works directly with Windows GUI
  - No Xvfb required for most operations
  - Use Windows paths and formats
  - PowerShell scripts for automation

For more information, see the documentation.
"@
    
    Write-Host $usageText
}

# Main execution
try {
    Write-Log "Starting AI Agent Windows container..."
    
    # Display container information
    Write-Log "Container Information:"
    Write-Log "  - PowerShell: $($PSVersionTable.PSVersion)"
    Write-Log "  - OS: $((Get-WmiObject -Class Win32_OperatingSystem).Caption)"
    Write-Log "  - User: $env:USERNAME"
    Write-Log "  - Working Directory: $(Get-Location)"
    
    # Validate environment if not skipped
    if (-not $SkipValidation) {
        Test-Environment
    }
    
    # Setup configuration
    Initialize-Configuration
    
    # Run health checks
    Test-Health
    
    # If no arguments provided, show usage
    if ($args.Count -eq 0) {
        Show-Usage
        exit 0
    }
    
    # Execute the command
    Write-Log "Executing: $($args -join ' ')"
    & $args[0] $args[1..($args.Length-1)]
    exit $LASTEXITCODE
}
catch {
    Write-Error "Container startup failed: $($_.Exception.Message)"
}

# Handle signals gracefully
try {
    $host.SetShouldExit($true)
}
catch {
    # Handle PowerShell exit gracefully
}
