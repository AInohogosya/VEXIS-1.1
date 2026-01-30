# AI Agent System

A production-ready vision-based AI agent system that automates GUI interactions through screenshot analysis and command execution.

## 🎯 Project Overview

This system implements a comprehensive AI agent that can:
- **See**: Capture and analyze screenshots in real-time
- **Think**: Use AI models to understand visual context and user instructions
- **Act**: Execute GUI automation commands with intelligent fallbacks
- **Learn**: Adapt strategies based on performance and context

## 🏗️ Architecture

The system follows a **4-layer architecture**:

### 1. User Interface Layer
- **Main Application**: Core CLI interface with comprehensive options
- **Enhanced Application**: Advanced features with conversation history
- **Shell Wrapper**: Safety validation and convenience wrapper

### 2. Core Processing Layer
- **Task Generation Engine**: Breaks down instructions into actionable steps
- **Command Parser**: Converts AI responses into executable commands
- **Execution Engine**: Executes commands with retry logic and fallbacks
- **Adaptive Strategy Manager**: Intelligent strategy selection and optimization

### 3. Platform Abstraction Layer
- **Screenshot Capture**: Cross-platform capture with multiple fallback methods
- **GUI Automation**: Cross-platform GUI automation with fallback mechanisms
- **Platform Detector**: Comprehensive system detection and configuration

### 4. External Integration Layer
- **Vision API Client**: Multi-provider AI model communication
- **Model Runner**: Unified interface for AI model interactions
- **API Manager**: Centralized API management with monitoring

### 5. Enhanced Context Management
- **Conversation History**: Temporal context tracking and management
- **Screenshot Labeling**: Visual context enhancement with labels

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Cross-platform GUI automation capabilities
- AI model API keys (OpenAI, Anthropic, etc.) or local Ollama setup

### Installation

#### Automatic Installation (Recommended)
```bash
# Clone the repository
git clone <repository-url>
cd ai-agent

# Run the installation script
./scripts/install/detect_os_and_install.sh
```

#### Manual Installation
```bash
# Create virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install the package
pip install -e .
```

### Basic Usage

```bash
# Simple instruction
ai-agent "Open a web browser and search for AI"

# Enhanced mode with conversation history
ai-agent-enhanced "Automate login process" --session-file session.json

# With custom configuration
ai-agent --config config.yaml "Click the button at coordinates (0.5, 0.3)"
```

## 🐳 Docker Support

### Quick Start with Docker Compose
```bash
# Start production containers
docker-compose --profile production up -d

# Start minimal container
docker-compose --profile minimal up -d

# Start development environment
docker-compose --profile development up -d
```

### Available Containers
- `ai-agent-ubuntu`: Full-featured Ubuntu-based container
- `ai-agent-centos`: Enterprise-ready CentOS container
- `ai-agent-alpine`: Minimal footprint Alpine container
- `ai-agent-macos`: macOS compatibility layer
- `ai-agent-windows`: Windows compatibility layer

## 📋 Features

### Core Capabilities
- **Vision-based Analysis**: Screenshot capture and AI-powered understanding
- **Cross-Platform Support**: macOS, Windows, Linux with automatic fallbacks
- **Intelligent Task Generation**: AI-powered breakdown of complex instructions
- **Robust Command Execution**: Multiple fallback methods with retry logic
- **Conversation History**: Context-aware execution with temporal understanding
- **Adaptive Strategies**: Machine learning-based strategy optimization

### Advanced Features
- **Screenshot Labeling**: Visual context enhancement with labels and annotations
- **Session Persistence**: Save and restore execution sessions
- **Multi-Model Support**: OpenAI, Anthropic, Google, local models
- **Performance Monitoring**: Comprehensive metrics and health checks
- **Security Hardening**: Input validation and error handling
- **Extensible Architecture**: Plugin system for custom components

## 🔧 Configuration

### Basic Configuration
```yaml
# config.yaml
logging:
  level: INFO
  console: true
  file: logs/ai_agent.log

api:
  timeout: 30
  max_retries: 3
  model: gpt-4-vision-preview

gui:
  click_delay: 0.1
  typing_delay: 0.05
  screenshot_quality: 95

security:
  max_coordinate_value: 1.0
  sanitize_text_input: true
```

### Environment Variables
```bash
export AI_AGENT_LOG_LEVEL=DEBUG
export AI_AGENT_CONFIG_PATH=/path/to/config.yaml
export OPENAI_API_KEY=your_api_key
export ANTHROPIC_API_KEY=your_api_key
```

## 🧪 Testing

### Run Tests
```bash
# Run all tests
pytest

# Run specific test categories
pytest tests/unit/
pytest tests/integration/
pytest tests/cross_platform/

# Run with coverage
pytest --cov=ai_agent --cov-report=html
```

### Test Categories
- **Unit Tests**: Component-level testing with mocking
- **Integration Tests**: End-to-end workflow testing
- **Cross-Platform Tests**: Platform compatibility validation
- **Performance Tests**: Resource usage and timing validation

## 📊 Monitoring

### Health Checks
```bash
# Check system health
ai-agent-validate

# Check API status
python -m ai_agent.external_integration.api_manager --check-health

# Check platform compatibility
python -m ai_agent.platform_abstraction.platform_detector --test
```

### Performance Metrics
```bash
# Get execution statistics
python -m ai_agent.core_processing.execution_engine --stats

# Get API performance
python -m ai_agent.external_integration.api_manager --performance

# Get strategy performance
python -m ai_agent.core_processing.adaptive_strategy_manager --stats
```

## 🔒 Security

### Security Features
- **Input Validation**: Comprehensive validation of all inputs
- **Command Sanitization**: Prevents dangerous command execution
- **Path Traversal Prevention**: Blocks directory traversal attacks
- **API Key Protection**: Secure credential management
- **Screenshot Privacy**: Optional screenshot redaction

### Security Best Practices
```bash
# Run in secure mode
ai-agent --validate-only

# Use configuration file with restricted permissions
chmod 600 config.yaml

# Enable security logging
AI_AGENT_LOG_LEVEL=DEBUG ai-agent "instruction"
```

## 📚 Documentation

### Architecture Documentation
- `docs/`: Additional documentation and guides

### API Documentation
```bash
# Generate API documentation
python -m ai_agent.main --help

# Enhanced app documentation
python -m ai_agent.enhanced --help
```

## 🤝 Contributing

### Development Setup
```bash
# Clone repository
git clone <repository-url>
cd ai-agent

# Setup development environment
./scripts/install/detect_os_and_install.sh
source .venv/bin/activate

# Install development dependencies
pip install -e ".[dev]"

# Run pre-commit hooks
pre-commit install
```

### Code Quality
```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/

# Run all checks
pre-commit run --all-files
```

### Submitting Changes
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## 🚨 Deployment

### Production Deployment
```bash
# Using Docker Compose
docker-compose --profile production up -d

# Using Docker
docker run -d \
  --name ai-agent-prod \
  -v /opt/ai-agent/logs:/app/logs \
  -v /opt/ai-agent/config.yaml:/app/config.yaml:ro \
  ai-agent:ubuntu
```

### Kubernetes Deployment
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ai-agent
spec:
  replicas: 3
  selector:
    matchLabels:
      app: ai-agent
  template:
    spec:
      containers:
      - name: ai-agent
        image: ai-agent:ubuntu
        ports:
        - containerPort: 8080
        env:
        - name: USE_XVFB
          value: "true"
```

## 🐛 Troubleshooting

### Common Issues

#### Installation Problems
```bash
# Check Python version
python3 --version

# Verify virtual environment
ls -la .venv/

# Check dependencies
pip list
```

#### Runtime Issues
```bash
# Check logs
tail -f logs/ai_agent.log

# Run diagnostics
ai-agent-validate

# Test components
python -c "import ai_agent; print('OK')"
```

#### Platform-Specific Issues
```bash
# Check platform detection
python -m ai_agent.platform_abstraction.platform_detector

# Test screenshot capture
python -m ai_agent.platform_abstraction.screenshot_capture --test

# Test GUI automation
python -m ai_agent.platform_abstraction.gui_automation --test
```

## 📄 Version History

### v1.0.0 (Current)
- Complete implementation of AI agent architecture
- Cross-platform support (macOS, Windows, Linux)
- Multi-model AI integration
- Enhanced context management
- Comprehensive testing suite
- Docker containerization
- Production-ready security features

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with comprehensive testing and validation
- Inspired by modern AI agent architectures
- Powered by cutting-edge computer vision and NLP technologies
- Community-driven development with extensive validation

## 📞 Support

For support, please:
1. Check the documentation
2. Search existing issues
3. Create a new issue with detailed information
4. Join our community discussions

---

**Built with ❤️ for flawless automation**
