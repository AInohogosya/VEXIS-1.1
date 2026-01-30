# AI Agent - CentOS Docker Container
# Zero-defect policy: comprehensive CentOS-based container with all dependencies

FROM centos:8

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Set labels
LABEL maintainer="AI Agent Team"
LABEL description="AI Agent - Vision-based GUI automation on CentOS"
LABEL version="1.0.0"

# Install system dependencies
RUN dnf update -y && \
    dnf groupinstall -y "Development Tools" && \
    dnf install -y \
    # Python and development tools
    python3.11 \
    python3.11-devel \
    python3-pip \
    python3-setuptools \
    python3-wheel \
    # System libraries for GUI automation and image processing
    mesa-libGL \
    glib2 \
    libSM \
    libXext \
    libXrender \
    libgomp \
    libXss \
    GConf2 \
    libXtst \
    alsa-lib \
    pango \
    atk \
    cairo \
    gdk-pixbuf2 \
    gtk3 \
    # X11 libraries for GUI automation
    xorg-x11-server-Xvfb \
    xorg-x11-utils \
    xorg-x11-xinit \
    # Additional libraries
    curl \
    wget \
    git \
    vim \
    htop \
    # EPEL repository for additional packages
    epel-release && \
    dnf clean all

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

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD .venv/bin/python -c "import ai_agent; print('AI Agent is healthy')" || exit 1

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Default command
CMD [".venv/bin/python", "-m", "ai_agent.main", "--help"]
