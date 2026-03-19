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
log() {
    echo "[INFO] $1"
}

error() {
    echo "[ERROR] $1" >&2
}

# ---------- check python ----------
if ! command -v python3 >/dev/null 2>&1; then
    error "Python3 is not installed."
    exit 1
fi

# ---------- create virtual environment ----------
if [ ! -d "$VENV_DIR" ]; then
    log "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# ---------- activate virtual environment ----------
log "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# ---------- install dependencies ----------
log "Installing dependencies..."
pip install --upgrade pip >/dev/null
pip install -r requirements.txt -q

# ---------- ensure directories ----------
log "Ensuring log directory exists..."
mkdir -p logs

# ---------- free port if already in use ----------
if lsof -i :"$APP_PORT" >/dev/null 2>&1; then
    log "Port $APP_PORT is in use. Stopping existing process..."
    lsof -ti :"$APP_PORT" | xargs kill -9 || true
fi

# ---------- start server ----------
log "Starting server..."
log "API:  http://localhost:$APP_PORT"
log "Docs: http://localhost:$APP_PORT/docs"

uvicorn "$APP_MODULE" \
    --reload \
    --host "$APP_HOST" \
    --port "$APP_PORT"