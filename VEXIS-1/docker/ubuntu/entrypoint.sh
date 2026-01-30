#!/bin/bash
# AI Agent Ubuntu Docker Entrypoint
# Zero-defect policy: robust container initialization with proper setup

set -euo pipefail

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >&2
}

# Error handling
error() {
    log "ERROR: $*"
    exit 1
}

# Function to start Xvfb for headless GUI operations
start_xvfb() {
    if [ "${USE_XVFB:-true}" = "true" ]; then
        log "Starting Xvfb for headless GUI operations..."
        
        # Set display
        export DISPLAY=${DISPLAY:-:99}
        
        # Start Xvfb with virtual screen
        Xvfb :99 -screen 0 1920x1080x24 -ac +extension GLX +render -noreset &
        XVFB_PID=$!
        
        # Wait for Xvfb to start
        sleep 2
        
        # Verify Xvfb is running
        if ! kill -0 $XVFB_PID 2>/dev/null; then
            error "Failed to start Xvfb"
        fi
        
        log "Xvfb started successfully (PID: $XVFB_PID)"
        
        # Set up trap to kill Xvfb on exit
        trap 'kill $XVFB_PID 2>/dev/null || true' EXIT
    else
        log "Skipping Xvfb (USE_XVFB=false)"
    fi
}

# Function to validate environment
validate_environment() {
    log "Validating environment..."
    
    # Check Python
    if ! command -v python3.11 >/dev/null 2>&1; then
        error "Python 3.11 not found"
    fi
    
    # Check virtual environment
    if [ ! -d "/app/.venv" ]; then
        error "Virtual environment not found"
    fi
    
    # Check AI Agent installation
    if ! /app/.venv/bin/python -c "import ai_agent" 2>/dev/null; then
        error "AI Agent not properly installed"
    fi
    
    log "Environment validation passed"
}

# Function to setup configuration
setup_configuration() {
    log "Setting up configuration..."
    
    # Create default config if not exists
    if [ ! -f "/app/config.yaml" ]; then
        log "Creating default configuration..."
        cat > /app/config.yaml << 'EOF'
logging:
  level: INFO
  console: true
  file: /app/logs/ai_agent.log
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
EOF
        chown aiagent:aiagent /app/config.yaml
    fi
    
    # Create log directory
    mkdir -p /app/logs
    chown aiagent:aiagent /app/logs
    
    # Create screenshots directory
    mkdir -p /app/screenshots
    chown aiagent:aiagent /app/screenshots
    
    log "Configuration setup completed"
}

# Function to run health checks
run_health_checks() {
    log "Running health checks..."
    
    # Check Python modules
    /app/.venv/bin/python -c "
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
    
    # Check AI Agent functionality
    /app/.venv/bin/python -c "
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
"
    
    log "Health checks completed"
}

# Function to display usage information
show_usage() {
    cat << 'EOF'
AI Agent Docker Container
========================

Usage Examples:
  # Show help
  docker run -it ai-agent-ubuntu --help
  
  # Run with instruction
  docker run -it --rm -v $(pwd)/screenshots:/app/screenshots ai-agent-ubuntu \
    "Open a web browser and search for AI"
  
  # Run enhanced mode with session persistence
  docker run -it --rm -v $(pwd)/sessions:/app/sessions ai-agent-ubuntu \
    python -m ai_agent.enhanced "Automate login process" --session-file /app/sessions/login.json
  
  # Run with custom configuration
  docker run -it --rm -v $(pwd)/config.yaml:/app/config.yaml ai-agent-ubuntu \
    "Click the button at coordinates (0.5, 0.3)"
  
  # Run tests
  docker run -it --rm ai-agent-ubuntu python -m pytest tests/
  
Environment Variables:
  - USE_XVFB: Enable/disable Xvfb (default: true)
  - DISPLAY: X11 display (default: :99)
  - AI_AGENT_LOG_LEVEL: Logging level (default: INFO)
  - AI_AGENT_CONFIG_PATH: Path to config file
  
Mount Points:
  - /app/screenshots: Screenshot output directory
  - /app/logs: Log files directory
  - /app/sessions: Session persistence directory
  - /app/config.yaml: Custom configuration file
  
For more information, see the documentation.
EOF
}

# Main execution
main() {
    log "Starting AI Agent Ubuntu container..."
    
    # Display container information
    log "Container Information:"
    log "  - Python: $(python3.11 --version)"
    log "  - OS: $(cat /etc/os-release | grep PRETTY_NAME | cut -d'=' -f2 | tr -d '"')"
    log "  - User: $(whoami)"
    log "  - Working Directory: $(pwd)"
    log "  - Display: ${DISPLAY:-not set}"
    
    # Validate environment
    validate_environment
    
    # Setup configuration
    setup_configuration
    
    # Start Xvfb if needed
    start_xvfb
    
    # Run health checks
    run_health_checks
    
    # If no arguments provided, show usage
    if [ $# -eq 0 ]; then
        show_usage
        exit 0
    fi
    
    # Execute the command
    log "Executing: $*"
    exec "$@"
}

# Handle signals gracefully
trap 'log "Received signal, shutting down..."; exit 0' SIGTERM SIGINT

# Run main function
main "$@"
