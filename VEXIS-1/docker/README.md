# AI Agent Docker Containers

This directory contains Docker configurations for running the AI Agent system across different platforms.

## Available Containers

### Platform-Specific Containers

| Container | Base Image | Platform | Size | Features |
|----------|------------|----------|------|----------|
| `ai-agent-ubuntu` | Ubuntu 22.04 | Linux | ~1.2GB | Full-featured with all dependencies |
| `ai-agent-centos` | CentOS 8 | Linux | ~1.1GB | Enterprise-ready with stable packages |
| `ai-agent-alpine` | Alpine 3.18 | Linux | ~800MB | Minimal footprint for resource-constrained environments |
| `ai-agent-macos` | Ubuntu 22.04 | macOS (cross-platform) | ~1.2GB | macOS compatibility layer |
| `ai-agent-windows` | Windows Server Core | Windows (cross-platform) | ~1.5GB | Windows compatibility layer |

### Specialized Containers

| Container | Purpose | Features |
|----------|---------|----------|
| `ai-agent-dev` | Development | Full source code mounting, debugging tools |
| `ai-agent-test` | Testing | Test framework, reporting, CI/CD integration |

## Quick Start

### Using Docker Compose (Recommended)

```bash
# Start all production containers
docker-compose --profile production up -d

# Start minimal container
docker-compose --profile minimal up -d

# Start development environment
docker-compose --profile development up -d

# Start testing environment
docker-compose --profile testing up
```

### Building Individual Containers

```bash
# Build Ubuntu container
docker build -f docker/ubuntu/Dockerfile -t ai-agent:ubuntu .

# Build Alpine container
docker build -f docker/alpine/Dockerfile -t ai-agent:alpine .

# Build Windows container (requires Windows host or buildx)
docker build -f docker/windows/Dockerfile -t ai-agent:windows .
```

## Usage Examples

### Basic Usage

```bash
# Run Ubuntu container with help
docker run -it --rm ai-agent:ubuntu --help

# Run with instruction
docker run -it --rm \
  -v $(pwd)/screenshots:/app/screenshots \
  ai-agent:ubuntu \
  "Open a web browser and search for AI"

# Run enhanced mode with session persistence
docker run -it --rm \
  -v $(pwd)/sessions:/app/sessions \
  ai-agent:ubuntu \
  python -m ai_agent.enhanced \
  "Automate login process" \
  --session-file /app/sessions/login.json
```

### Development Workflow

```bash
# Start development environment
docker-compose --profile development up -d

# Execute commands in running container
docker-compose exec ai-agent-dev bash

# Run tests
docker-compose exec ai-agent-dev python -m pytest tests/

# Install new dependencies
docker-compose exec ai-agent-dev pip install new-package
```

### Testing

```bash
# Run all tests
docker-compose --profile testing up

# Run specific test file
docker-compose exec ai-agent-test python -m pytest tests/unit/test_validation.py

# Generate test report
docker-compose exec ai-agent-test python -m pytest tests/ --html=/app/test-results/report.html
```

## Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|------------|
| `USE_XVFB` | `true` | Enable/disable Xvfb for headless GUI operations |
| `DISPLAY` | `:99` | X11 display number |
| `AI_AGENT_LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL) |
| `AI_AGENT_CONFIG_PATH` | `/app/config.yaml` | Path to configuration file |
| `AI_AGENT_PLATFORM` | `auto` | Force platform detection |
| `AI_AGENT_TEST_MODE` | `false` | Enable test mode |

### Volume Mounts

| Mount Point | Purpose | Example |
|-------------|---------|---------|
| `/app/logs` | Log files | `./logs:/app/logs` |
| `/app/screenshots` | Screenshot output | `./screenshots:/app/screenshots` |
| `/app/sessions` | Session persistence | `./sessions:/app/sessions` |
| `/app/config.yaml` | Configuration | `./config.yaml:/app/config.yaml:ro` |
| `/app` | Source code (dev only) | `.:/app:delegated` |

## Platform-Specific Notes

### Ubuntu/CentOS
- Full GUI automation support
- Xvfb for headless operations
- Complete dependency set
- Recommended for production

### Alpine
- Minimal footprint
- Faster startup
- Reduced dependency set
- Suitable for resource-constrained environments

### macOS (Cross-Platform)
- Linux container with macOS compatibility layer
- Simulates macOS-specific behaviors
- For development/testing on Linux systems

### Windows (Cross-Platform)
- Linux container with Windows compatibility layer
- Simulates Windows-specific behaviors
- For development/testing on Linux systems

## Health Checks

All containers include health checks that verify:
- Python environment is functional
- Required modules are importable
- AI Agent core functionality works
- Configuration is loadable

```bash
# Check container health
docker ps --format "table {{.Names}}\t{{.Status}}"
docker inspect ai-agent-ubuntu --format='{{json .State.Health}}'
```

## Troubleshooting

### Common Issues

#### Container Won't Start
```bash
# Check logs
docker logs ai-agent-ubuntu

# Check health status
docker inspect ai-agent-ubuntu --format='{{json .State.Health}}'
```

#### GUI Automation Issues
```bash
# Ensure Xvfb is running
docker exec ai-agent-ubuntu ps aux | grep Xvfb

# Check display variables
docker exec ai-agent-ubuntu env | grep DISPLAY
```

#### Permission Issues
```bash
# Check user permissions
docker exec ai-agent-ubuntu id

# Fix volume permissions
sudo chown -R 1000:1000 ./logs ./screenshots ./sessions
```

### Performance Optimization

#### Resource Limits
```yaml
# docker-compose.yml
services:
  ai-agent-ubuntu:
    deploy:
      resources:
        limits:
          memory: 2G
          cpus: '1.0'
        reservations:
          memory: 1G
          cpus: '0.5'
```

#### Build Optimization
```bash
# Use build cache effectively
docker build --build-arg BUILDKIT_INLINE_CACHE=1 -f docker/ubuntu/Dockerfile .

# Multi-stage builds for smaller images
docker build --target=runtime -f docker/ubuntu/Dockerfile .
```

## Security Considerations

### Container Security
- Run as non-root user (`aiagent`)
- Read-only configuration mounts where possible
- Limit container capabilities
- Use specific image tags (avoid `latest`)

### Network Security
- Use custom Docker networks
- Limit exposed ports
- Implement proper authentication for web interfaces

### Data Security
- Encrypt sensitive configuration
- Use volume encryption for persistent data
- Regular security updates for base images

## CI/CD Integration

### GitHub Actions
```yaml
name: Test AI Agent
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build and test
        run: |
          docker-compose --profile testing build
          docker-compose --profile testing up
          docker-compose exec ai-agent-test python -m pytest tests/
```

### Jenkins Pipeline
```groovy
pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'docker-compose --profile testing build'
            }
        }
        stage('Test') {
            steps {
                sh 'docker-compose --profile testing up'
                sh 'docker-compose exec ai-agent-test python -m pytest tests/'
            }
        }
    }
}
```

## Development Workflow

### Local Development
```bash
# Clone repository
git clone <repository-url>
cd ai-agent

# Start development environment
docker-compose --profile development up -d

# Work on code
docker-compose exec ai-agent-dev bash

# Run tests
docker-compose exec ai-agent-dev python -m pytest tests/

# Stop environment
docker-compose --profile development down
```

### Multi-Platform Testing
```bash
# Test all platforms
docker-compose --profile cross-platform build

# Run tests on each platform
for platform in ubuntu centos alpine; do
    echo "Testing $platform platform..."
    docker run --rm ai-agent:$platform python -m pytest tests/unit/
done
```

## Production Deployment

### Single Container Deployment
```bash
# Pull latest image
docker pull ai-agent:ubuntu

# Run with production configuration
docker run -d \
  --name ai-agent-prod \
  -v /opt/ai-agent/logs:/app/logs \
  -v /opt/ai-agent/screenshots:/app/screenshots \
  -v /opt/ai-agent/config.yaml:/app/config.yaml:ro \
  ai-agent:ubuntu
```

### Swarm Deployment
```yaml
version: '3.8'
services:
  ai-agent:
    image: ai-agent:ubuntu
    deploy:
      replicas: 3
      update_config:
        parallelism: 1
        delay: 10s
      restart_policy:
        condition: on-failure
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
    metadata:
      labels:
        app: ai-agent
    spec:
      containers:
      - name: ai-agent
        image: ai-agent:ubuntu
        ports:
        - containerPort: 8080
        env:
        - name: USE_XVFB
          value: "true"
        volumeMounts:
        - name: logs
          mountPath: /app/logs
      volumes:
      - name: logs
        persistentVolumeClaim:
          claimName: ai-agent-logs
```

## Monitoring and Logging

### Log Collection
```bash
# View logs
docker-compose logs -f ai-agent-ubuntu

# Follow specific service logs
docker-compose logs -f ai-agent-dev

# Export logs
docker logs ai-agent-ubuntu > ai-agent.log 2>&1
```

### Metrics Collection
```bash
# Resource usage
docker stats ai-agent-ubuntu

# Container inspection
docker inspect ai-agent-ubuntu --format='{{json .State}}'
```

## Support

For issues with Docker containers:
1. Check container logs: `docker logs <container-name>`
2. Verify health status: `docker inspect <container-name>`
3. Check resource usage: `docker stats <container-name>`
4. Review configuration: `docker exec <container-name> cat /app/config.yaml`

For issues with the AI Agent itself:
1. Check the GitHub Issues page
2. Review the documentation
3. Run with debug logging: `AI_AGENT_LOG_LEVEL=DEBUG`
4. Enable test mode: `AI_AGENT_TEST_MODE=true`
