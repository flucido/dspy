#!/bin/bash
# Start the Ox-Turn API server
# Usage: ./run_api.sh [--reload]

cd "$(dirname "$0")"

if [ "$1" = "--reload" ]; then
    echo "Starting Ox-Turn API in development mode (with auto-reload)..."
    uv run uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload
else
    echo "Starting Ox-Turn API..."
    uv run uvicorn api.main:app --host 0.0.0.0 --port 8000
fi
