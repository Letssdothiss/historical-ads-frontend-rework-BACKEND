#!/usr/bin/env bash
set -e

# ==================================================
# Historical Job Listings Backend - Startup Script
# ==================================================

APP_HOST="0.0.0.0"
APP_PORT="8000"
APP_MODULE="app.main:app"
VENV_DIR="venv"

# ---------- logging helpers ----------
log() { echo "[INFO] $1"; }
error() { echo "[ERROR] $1" >&2; }

# ---------- detect python ----------
# Windows Git Bash has issues with the python alias -> fallback to full path
if [[ "$OSTYPE" == "msys"* || "$OSTYPE" == "win32"* ]]; then
    # Specify your Python path here
    PYTHON="/c/Python312/python.exe"
else
    # Linux/macOS
    if command -v python3 >/dev/null 2>&1; then
        PYTHON=python3
    elif command -v python >/dev/null 2>&1; then
        PYTHON=python
    else
        error "Python is not installed."
        exit 1
    fi
fi

log "Using Python: $($PYTHON --version 2>&1)"

# ---------- create virtual environment ----------
if [ ! -d "$VENV_DIR" ]; then
    log "Creating virtual environment..."
    $PYTHON -m venv "$VENV_DIR"
fi

# ---------- activate virtual environment ----------
if [ -f "$VENV_DIR/bin/activate" ]; then
    source "$VENV_DIR/bin/activate"
elif [ -f "$VENV_DIR/Scripts/activate" ]; then
    source "$VENV_DIR/Scripts/activate"
else
    error "Virtual environment activation script not found."
    exit 1
fi

# ---------- install dependencies ----------
log "Installing dependencies..."
# On Windows, pip may need full path
if [[ "$OSTYPE" == "msys"* || "$OSTYPE" == "win32"* ]]; then
    "$VENV_DIR/Scripts/python.exe" -m pip install --upgrade pip
    "$VENV_DIR/Scripts/python.exe" -m pip install -r requirements.txt -q
else
    pip install --upgrade pip >/dev/null
    pip install -r requirements.txt -q
fi

# ---------- ensure directories ----------
log "Ensuring log directory exists..."
mkdir -p logs

# ---------- free port if already in use ----------
if command -v lsof >/dev/null 2>&1; then
    if lsof -i :"$APP_PORT" >/dev/null 2>&1; then
        log "Port $APP_PORT is in use. Stopping existing process..."
        lsof -ti :"$APP_PORT" | xargs kill -9 || true
    fi
fi

# ---------- start server ----------
log "Starting server..."
log "API:  http://localhost:$APP_PORT"
log "Docs: http://localhost:$APP_PORT/docs"

uvicorn "$APP_MODULE" \
    --reload \
    --host "$APP_HOST" \
    --port "$APP_PORT"