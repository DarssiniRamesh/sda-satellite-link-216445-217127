#!/usr/bin/env sh
set -e

PORT="${PORT:-5000}"
HOST="${HOST:-0.0.0.0}"

# If running locally (not in container), ensure deps are installed.
if [ -f "requirements.txt" ]; then
  echo "Installing Python dependencies from requirements.txt (if needed)..."
  python -m pip install --upgrade pip >/dev/null 2>&1 || true
  python -m pip install --no-cache-dir -r requirements.txt
fi

echo "Starting ManagementandControlService on ${HOST}:${PORT}"
exec uvicorn main:app --host "${HOST}" --port "${PORT}"
