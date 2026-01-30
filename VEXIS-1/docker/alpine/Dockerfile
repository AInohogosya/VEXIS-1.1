# AI Agent - Alpine Docker Container
# Zero-defect policy: minimal Alpine-based container with all dependencies

FROM alpine:3.18

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

# Set labels
LABEL maintainer="AI Agent Team"
LABEL description="AI Agent - Vision-based GUI automation on Alpine"
LABEL version="1.0.0"

# Install system dependencies
RUN apk add --no-cache \
    # Python and development tools
    python3 \
    python3-dev \
    py3-pip \
    # Build tools
    gcc \
    musl-dev \
    linux-headers \
    # System libraries for GUI automation and image processing
    mesa-gl \
    glib \
    libsm \
    libxext \
    libxrender \
    libgomp \
    libxss \
    # X11 libraries for GUI automation
    xvfb \
    xorg-server \
    xorg-server-xvfb \
    # Additional libraries
    curl \
    wget \
    git \
    vim \
    htop \
    # Font support
    fontconfig \
    ttf-liberation \
    ttf-dejavu \
    # Clean up
    && apk del --purge \
        python3-dev \
        gcc \
        musl-dev \
        linux-headers \
    && rm -rf /var/cache/apk/*

# Create non-root user for security
RUN addgroup -g 1000 aiagent && \
    adduser -D -u 1000 -G aiagent -s /bin/bash aiagent

# Set working directory
WORKDIR /app

# Copy requirements first (for better layer caching)
COPY requirements.txt pyproject.toml ./

# Install Python dependencies
RUN python3 -m venv .venv && \
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
    .venv/bin/python -c "import ai_agent; print('AI Agent is healthy')" || exit 1

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Default command
CMD [".venv/bin/python", "-m", "ai_agent.main", "--help"]
