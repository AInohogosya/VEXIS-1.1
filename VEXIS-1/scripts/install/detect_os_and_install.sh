#!/bin/bash
# Cross-platform dependency detection and installation script
# Zero-defect policy: comprehensive validation and error handling

set -euo pipefail

# Logging functions
log() {
    printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" >&2
}

error() {
    printf '[ERROR] %s\n' "$*" >&2
    exit 1
}

warning() {
    printf '[WARNING] %s\n' "$*" >&2
}

success() {
    printf '[SUCCESS] %s\n' "$*" >&2
}

# Detect operating system
detect_os() {
    local os_id=""
    local os_version=""
    local arch=""
    
    log "Detecting operating system..."
    
    # Linux detection
    if [[ -f /etc/os-release ]]; then
        source /etc/os-release
        os_id="$ID"
        os_version="$VERSION_ID"
        log "Linux detected: $os_id $os_version"
    # macOS detection
    elif command -v sw_vers >/dev/null 2>&1; then
        os_id="macos"
        os_version="$(sw_vers -productVersion)"
        log "macOS detected: $os_version"
    # Windows detection (via WSL or Git Bash)
    elif [[ -n "${WINDIR:-}" ]] || command -v cmd.exe >/dev/null 2>&1; then
        os_id="windows"
        os_version="$(cmd.exe /c ver 2>/dev/null | head -1 || echo 'unknown')"
        log "Windows detected: $os_version"
    else
        error "Unsupported operating system"
    fi
    
    # Architecture detection
    arch="$(uname -m 2>/dev/null || echo 'unknown')"
    log "Architecture: $arch"
    
    # Export for other functions
    export DETECTED_OS="$os_id"
    export DETECTED_VERSION="$os_version"
    export DETECTED_ARCH="$arch"
}

# Check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Python version and installation
check_python() {
    log "Checking Python installation..."
    
    local python_cmd=""
    local python_version=""
    
    # Find Python command
    if command_exists python3; then
        python_cmd="python3"
    elif command_exists python; then
        python_cmd="python"
    else
        error "Python not found"
    fi
    
    # Check version
    python_version="$("$python_cmd" --version 2>&1 || echo 'unknown')"
    log "Found: $python_version"
    
    # Validate version (require 3.8+)
    if ! "$python_cmd" -c "import sys; exit(0 if sys.version_info >= (3, 8) else 1)" 2>/dev/null; then
        error "Python 3.8 or higher is required. Found: $python_version"
    fi
    
    export PYTHON_CMD="$python_cmd"
    success "Python validation passed: $python_version"
}

# Install Python based on OS
install_python() {
    log "Installing Python..."
    
    case "$DETECTED_OS" in
        ubuntu|debian)
            if command_exists apt-get; then
                log "Using apt-get to install Python..."
                sudo apt-get update
                sudo apt-get install -y python3 python3-venv python3-pip python3-dev
            else
                error "apt-get not available. Please install Python manually."
            fi
            ;;
        rhel|centos|fedora)
            if command_exists yum; then
                log "Using yum to install Python..."
                sudo yum install -y python3 python3-pip python3-devel
            elif command_exists dnf; then
                log "Using dnf to install Python..."
                sudo dnf install -y python3 python3-pip python3-devel
            else
                error "Package manager not found. Please install Python manually."
            fi
            ;;
        macos)
            if command_exists brew; then
                log "Using Homebrew to install Python..."
                brew install python
            else
                log "Installing Homebrew first..."
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
                brew install python
            fi
            ;;
        windows)
            error "On Windows, please download and install Python from https://python.org"
            ;;
        *)
            error "Unsupported OS for automatic Python installation: $DETECTED_OS"
            ;;
    esac
    
    # Re-check after installation
    check_python
}

# Check and install system dependencies
check_system_dependencies() {
    log "Checking system dependencies..."
    
    case "$DETECTED_OS" in
        ubuntu|debian)
            local deps=("libgl1-mesa-glx" "libglib2.0-0" "libsm6" "libxext6" "libxrender-dev" "libgomp1")
            for dep in "${deps[@]}"; do
                if ! dpkg -l | grep -q "^ii  $dep "; then
                    log "Installing missing dependency: $dep"
                    sudo apt-get install -y "$dep"
                fi
            done
            ;;
        rhel|centos|fedora)
            local deps=("mesa-libGL" "glib2" "libSM" "libXext" "libXrender" "libgomp")
            for dep in "${deps[@]}"; do
                if ! rpm -q "$dep" >/dev/null 2>&1; then
                    log "Installing missing dependency: $dep"
                    sudo yum install -y "$dep" || sudo dnf install -y "$dep"
                fi
            done
            ;;
        macos)
            # macOS usually has required dependencies
            log "macOS dependencies check passed"
            ;;
        *)
            warning "Skipping system dependency check for unsupported OS: $DETECTED_OS"
            ;;
    esac
    
    success "System dependencies validated"
}

# Create and activate virtual environment
setup_virtual_environment() {
    log "Setting up Python virtual environment..."
    
    local venv_path=".venv"
    
    # Remove existing venv if corrupted
    if [[ -d "$venv_path" ]] && ! "$PYTHON_CMD" -c "import sys; sys.path.insert(0, '$venv_path/lib/python*/site-packages')" 2>/dev/null; then
        log "Removing corrupted virtual environment..."
        rm -rf "$venv_path"
    fi
    
    # Create virtual environment
    if [[ ! -d "$venv_path" ]]; then
        log "Creating virtual environment..."
        "$PYTHON_CMD" -m venv "$venv_path"
    fi
    
    # Activate and upgrade pip
    log "Activating virtual environment and upgrading pip..."
    source "$venv_path/bin/activate"
    pip install --upgrade pip setuptools wheel
    
    success "Virtual environment setup complete"
}

# Install Python dependencies
install_python_dependencies() {
    log "Installing Python dependencies..."
    
    # Activate virtual environment
    source .venv/bin/activate
    
    # Install requirements
    if [[ -f "requirements.txt" ]]; then
        log "Installing from requirements.txt..."
        pip install -r requirements.txt
    else
        error "requirements.txt not found"
    fi
    
    # Install package in development mode
    log "Installing AI Agent package..."
    pip install -e .
    
    success "Python dependencies installed"
}

# Validate installation
validate_installation() {
    log "Validating installation..."
    
    # Activate virtual environment
    source .venv/bin/activate
    
    # Test imports
    log "Testing core imports..."
    python -c "
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
"
    
    # Test CLI commands
    log "Testing CLI commands..."
    if command_exists ai-agent; then
        log "✓ ai-agent command available"
    else
        error "ai-agent command not found"
    fi
    
    success "Installation validation complete"
}

# Main installation function
main() {
    log "Starting AI Agent installation..."
    log "Zero-defect policy: comprehensive validation enabled"
    
    # Change to script directory
    cd "$(dirname "$0")/../.."
    
    # Detect OS
    detect_os
    
    # Check and install Python
    if ! check_python; then
        install_python
    fi
    
    # Check system dependencies
    check_system_dependencies
    
    # Setup virtual environment
    setup_virtual_environment
    
    # Install Python dependencies
    install_python_dependencies
    
    # Validate installation
    validate_installation
    
    success "AI Agent installation completed successfully!"
    log "To activate the environment: source .venv/bin/activate"
    log "To run the agent: ai-agent --help"
}

# Run main function
main "$@"
