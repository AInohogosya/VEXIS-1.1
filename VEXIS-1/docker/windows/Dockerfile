# AI Agent - Windows Docker Container
# Zero-defect policy: comprehensive Windows-based container with all dependencies

FROM mcr.microsoft.com/windows/servercore:ltsc2022

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Set labels
LABEL maintainer="AI Agent Team"
LABEL description="AI Agent - Vision-based GUI automation on Windows"
LABEL version="1.0.0"

# Install Chocolatey
RUN powershell -Command \
    Set-ExecutionPolicy Bypass -Scope Process -Force; \
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072 -bor 192 -bor 768 -bor -ssl3 -bor 192 -bor 128 -bor 256; \
    iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Install Python and dependencies
RUN powershell -Command \
    choco install -y python311 --version=3.11.7; \
    choco install -y git; \
    choco install -y visualstudio2022buildtools --package-parameters "--add Microsoft.VisualStudio.Component.VC.Tools.x86.x64"; \
    choco install -y vcredist2008; \
    refreshenv

# Create application directory
RUN powershell -Command \
    New-Item -ItemType Directory -Path "C:\app" -Force; \
    New-Item -ItemType Directory -Path "C:\app\logs" -Force; \
    New-Item -ItemType Directory -Path "C:\app\screenshots" -Force; \
    New-Item -ItemType Directory -Path "C:\app\data" -Force; \
    New-Item -ItemType Directory -Path "C:\app\temp" -Force

# Set working directory
WORKDIR C:\app

# Copy requirements and configuration files
COPY requirements.txt .
COPY pyproject.toml .
COPY src\ src\
COPY scripts\ scripts\
COPY config\ config\

# Create virtual environment and install Python dependencies
RUN powershell -Command \
    python -m venv .venv; \
    .venv\Scripts\pip install --upgrade pip setuptools wheel; \
    .venv\Scripts\pip install --no-cache-dir -r requirements.txt

# Install the application in development mode
RUN powershell -Command \
    .venv\Scripts\pip install -e .

# Copy entrypoint script
COPY docker\entrypoint.ps1 C:\entrypoint.ps1

# Expose port for potential web interface
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD powershell -Command ".venv\Scripts\python -c \"import ai_agent; print('AI Agent is healthy')\"" || exit 1

# Set entrypoint
ENTRYPOINT ["powershell", "-File", "C:\\entrypoint.ps1"]

# Default command
CMD [".venv\\Scripts\\python", "-m", "ai_agent.main", "--help"]
