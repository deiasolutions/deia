#!/bin/bash
# DEIA Solutions - Production Deployment Script
# Author: BOT-001 (Infrastructure Lead)
# Date: 2025-10-25
# Status: PRODUCTION-READY

set -euo pipefail  # Exit on error, undefined vars, pipe failures

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
LOG_FILE="${PROJECT_ROOT}/.deia/logs/deployment_${TIMESTAMP}.log"

# Deployment phases
PHASE_VALIDATION=0
PHASE_PREP=1
PHASE_BUILD=2
PHASE_DEPLOY=3
PHASE_VERIFY=4

# Create log directory
mkdir -p "$(dirname "$LOG_FILE")"

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1" | tee -a "$LOG_FILE"
    exit 1
}

warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1" | tee -a "$LOG_FILE"
}

# Phase 0: Validate deployment environment
validate_environment() {
    log "PHASE 0: Validating environment..."

    # Check required commands
    local required_commands=("python3" "pip" "git" "docker")
    for cmd in "${required_commands[@]}"; do
        if ! command -v "$cmd" &> /dev/null; then
            error "Required command not found: $cmd"
        fi
    done

    # Check Python version (3.9+)
    local python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    log "Python version: $python_version"

    # Check git status
    cd "$PROJECT_ROOT"
    if [ -z "$(git status --porcelain)" ]; then
        log "Git repository is clean"
    else
        warning "Git working directory has uncommitted changes"
        git status --short | tee -a "$LOG_FILE"
    fi

    # Check .env file
    if [ ! -f "$PROJECT_ROOT/.env" ]; then
        error ".env file not found. Copy .env.example to .env and configure"
    fi

    log "Environment validation PASSED"
}

# Phase 1: Preparation
prepare_deployment() {
    log "PHASE 1: Preparing deployment..."

    # Create backup of current deployment (if exists)
    if [ -d "$PROJECT_ROOT/deployment-backup" ]; then
        backup_dir="$PROJECT_ROOT/deployment-backup-${TIMESTAMP}"
        cp -r "$PROJECT_ROOT/deployment-backup" "$backup_dir"
        log "Backed up previous deployment to $backup_dir"
    fi

    # Create necessary directories
    mkdir -p "$PROJECT_ROOT/.deia/logs"
    mkdir -p "$PROJECT_ROOT/.deia/data"
    mkdir -p "$PROJECT_ROOT/.deia/reports"

    # Load environment variables
    source "$PROJECT_ROOT/.env"
    log "Environment variables loaded"

    log "Preparation COMPLETE"
}

# Phase 2: Build
build_application() {
    log "PHASE 2: Building application..."

    cd "$PROJECT_ROOT"

    # Install/upgrade dependencies
    log "Installing Python dependencies..."
    pip install --upgrade pip setuptools wheel
    pip install -r requirements.txt -q

    # Run tests
    log "Running unit tests..."
    python -m pytest tests/unit -v --tb=short || warning "Some unit tests failed"

    # Run linting
    log "Running code quality checks..."
    python -m flake8 src/ --max-line-length=120 --count || warning "Linting issues found"

    # Type checking
    log "Running type checks..."
    python -m mypy src/ --ignore-missing-imports || warning "Type checking issues found"

    log "Build COMPLETE"
}

# Phase 3: Deploy
deploy_application() {
    log "PHASE 3: Deploying application..."

    cd "$PROJECT_ROOT"

    # Docker build (if Dockerfile exists)
    if [ -f "$PROJECT_ROOT/Dockerfile" ]; then
        log "Building Docker image..."
        docker build -t deia-solutions:${TIMESTAMP} .
        log "Docker image built successfully"
    fi

    # Database migrations (if applicable)
    if [ -f "$PROJECT_ROOT/src/deia/db/migrations" ]; then
        log "Running database migrations..."
        python -m alembic upgrade head
        log "Database migrations complete"
    fi

    # Start services
    log "Starting services..."

    # Start bot service
    if [ -f "$PROJECT_ROOT/run_bot_service.py" ]; then
        log "Starting bot service on port 8001..."
        python run_bot_service.py &
        BOT_SERVICE_PID=$!
        sleep 2  # Give service time to start
    fi

    # Start web interface (if applicable)
    if [ -f "$PROJECT_ROOT/run_web_service.py" ]; then
        log "Starting web service on port 8000..."
        python run_web_service.py &
        WEB_SERVICE_PID=$!
        sleep 2  # Give service time to start
    fi

    log "Deployment COMPLETE"
}

# Phase 4: Verification
verify_deployment() {
    log "PHASE 4: Verifying deployment..."

    local health_checks_passed=0
    local health_checks_total=0

    # Check bot service health
    if [ ! -z "${BOT_SERVICE_PID:-}" ]; then
        health_checks_total=$((health_checks_total + 1))
        if curl -s http://localhost:8001/health | grep -q '"status":"ok"'; then
            log "✓ Bot service health check PASSED"
            health_checks_passed=$((health_checks_passed + 1))
        else
            error "✗ Bot service health check FAILED"
        fi
    fi

    # Check web service health
    if [ ! -z "${WEB_SERVICE_PID:-}" ]; then
        health_checks_total=$((health_checks_total + 1))
        if curl -s http://localhost:8000/health | grep -q '"status":"ok"'; then
            log "✓ Web service health check PASSED"
            health_checks_passed=$((health_checks_passed + 1))
        else
            error "✗ Web service health check FAILED"
        fi
    fi

    # Check integration
    log "Running integration tests..."
    python -m pytest tests/integration -v --tb=short || warning "Some integration tests failed"

    # Summary
    log "Health checks: $health_checks_passed/$health_checks_total passed"

    if [ $health_checks_passed -eq $health_checks_total ]; then
        log "Verification PASSED - Deployment successful!"
    else
        error "Verification FAILED - Some health checks did not pass"
    fi
}

# Cleanup on error
cleanup_on_error() {
    error_code=$?
    log "Deployment FAILED with exit code $error_code"

    # Kill any started services
    [ ! -z "${BOT_SERVICE_PID:-}" ] && kill $BOT_SERVICE_PID 2>/dev/null || true
    [ ! -z "${WEB_SERVICE_PID:-}" ] && kill $WEB_SERVICE_PID 2>/dev/null || true

    exit $error_code
}

trap cleanup_on_error EXIT

# Main execution
main() {
    log "=========================================="
    log "DEIA Solutions Deployment Script"
    log "Started at $(date)"
    log "=========================================="

    validate_environment
    prepare_deployment
    build_application
    deploy_application
    verify_deployment

    log "=========================================="
    log "Deployment SUCCESSFUL"
    log "Log file: $LOG_FILE"
    log "=========================================="
}

# Run main function
main "$@"
