# Open Source Setup Instructions

## Quick Start

This repository is configured for easy open-source installation with minimal dependencies.

### Prerequisites

1. **Python 3.8+** installed
2. **Virtual environment support** (install if missing):
   ```bash
   # Ubuntu/Debian:
   sudo apt install python3-venv
   
   # macOS (usually included with Python):
   # No additional installation needed
   
   # Windows:
   # Usually included with Python installation
   ```

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd VEXIS-1
   ```

2. **Run the auto-setup script:**
   ```bash
   python3 run.py "your instruction here"
   ```
   
   The script will automatically:
   - Create a virtual environment
   - Install core dependencies
   - Start the AI agent

### Dependencies

#### Core Dependencies (Auto-installed)
- Basic GUI automation (pyautogui, pynput)
- Screenshot capture (Pillow, opencv-python)
- API communication (requests, ollama)
- Configuration management (PyYAML, pydantic)

#### Optional Dependencies (Manual install)
For advanced AI/ML features:
```bash
pip install -r requirements-optional.txt
```

This includes:
- OpenAI and Anthropic API clients
- Transformers and PyTorch for local ML models
- Development tools (pytest, black, mypy)

### Configuration

1. **Copy the example configuration:**
   ```bash
   cp config.yaml.example config.yaml
   ```

2. **Edit `config.yaml`** to set your preferred AI provider and models.

### Usage Examples

```bash
# Basic GUI automation
python3 run.py "Take a screenshot and save it"

# Web automation
python3 run.py "Open a browser and search for AI"

# File operations
python3 run.py "Create a new text file with hello world"
```

### Troubleshooting

#### Virtual Environment Issues
If you get "ensurepip is not available" error:
```bash
sudo apt install python3-venv  # Ubuntu/Debian
```

#### GUI Automation Issues
- **Linux**: Install tkinter for mouse info:
  ```bash
  sudo apt install python3-tk python3-dev
  ```
- **macOS**: Grant accessibility permissions in System Preferences
- **Windows**: Run as administrator if needed

#### Permission Issues
Make sure you have write permissions to the project directory.

### Development Setup

For contributing to the project:

1. **Install development dependencies:**
   ```bash
   pip install -r requirements-optional.txt
   ```

2. **Install pre-commit hooks:**
   ```bash
   pre-commit install
   ```

3. **Run tests:**
   ```bash
   pytest
   ```

### Project Structure

```
VEXIS-1/
├── run.py                 # Main entry point with auto-setup
├── config.yaml           # Configuration file
├── requirements-core.txt # Core dependencies
├── requirements-optional.txt # Optional ML/AI deps
├── src/                  # Source code
├── scripts/              # Utility scripts
└── docs/                 # Documentation
```

### Security Note

This repository contains no personal information, API keys, or sensitive data. All configuration uses environment variables or example values.
