# AI Agent - macOS Docker Container
# Zero-defect policy: comprehensive macOS-based container with all dependencies

FROM --platform=linux/amd64 ubuntu:22.4

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Set labels
LABEL maintainer="AI Agent Team"
LABEL description="AI Agent - Vision-based GUI automation (macOS cross-platform)"
LABEL version="1.0.0"
LABEL platform="linux/amd64"

# Install system dependencies
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y \
    # Python and development tools
    python3.11 \
    python3.11-dev \
    python3.11-venv \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    # System libraries for GUI automation and image processing
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libxss1 \
    libgconf-2-4 \
    libxtst6 \
    libasound2 \
    libpangocairo-1.0-0 \
    libatk1.0-0 \
    libcairo-gobject2 \
    libgtk-3-0 \
    libgdk-pixbuf2.0-0 \
    # X11 libraries for GUI automation
    xvfb \
    x11-utils \
    x11-xserver-utils \
    # Additional libraries
    curl \
    wget \
    git \
    vim \
    htop \
    # Clean up
    && apt-get autoremove -y \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN groupadd -r aiagent && \
    useradd -r -g aiagent -d /app -s /bin/bash aiagent

# Set working directory
WORKDIR /app

# Copy requirements first (for better layer caching)
COPY requirements.txt pyproject.toml ./

# Create virtual environment and install Python dependencies
RUN python3.11 -m venv .venv && \
    .venv/bin/pip install --upgrade pip setuptools wheel && \
    .venv/bin/pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY scripts/ ./scripts/
COPY config/ ./config/

# Install the application in development mode
RUN .venv/bin/pip install -e .

# Create necessary directories
RUN mkdir -p /app/logs /app/screenshots /app/data /app/temp && \
    chown -R aiagent:aiagent /app

# Copy entrypoint script
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Switch to non-root user
USER aiagent

# Expose port for potential web interface
EXPOSE 8080

# Set default environment variables for headless operation
ENV DISPLAY=:99
ENV QT_QPA_PLATFORM=offscreen
ENV SDL_VIDEODRIVER=dummy

# macOS-specific environment variables (for compatibility)
ENV AI_AGENT_PLATFORM=macos
ENV AI_AGENT_MACOS_COMPATIBILITY=true

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD .venv/bin/python -c "import ai_agent; print('AI Agent is healthy')" || exit 1

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Default command
CMD [".venv/bin/python", "-m", "ai_agent.main", "--help"]
