#!/usr/bin/env sh
# PUBLIC_INTERFACE
# Simple bootstrap script to install dependencies and start the service with uvicorn.
# Usage:
#   ./bootstrap.sh            # installs deps and runs on 0.0.0.0:5000
#   PORT=8000 HOST=127.0.0.1 ./bootstrap.sh
set -e

PORT="${PORT:-5000}"
HOST="${HOST:-0.0.0.0}"

if [ -f "requirements.txt" ]; then
  echo "Installing Python dependencies from requirements.txt..."
  python -m pip install --upgrade pip >/dev/null 2>&1 || true
  python -m pip install --no-cache-dir -r requirements.txt
fi

echo "Validating FastAPI import..."
python - <<'PYCODE'
try:
    import fastapi  # noqa: F401
    print("FastAPI import OK")
except Exception as e:
    raise SystemExit(f"FastAPI import failed: {e}")
PYCODE

echo "Starting uvicorn main:app on ${HOST}:${PORT}..."
exec uvicorn main:app --host "${HOST}" --port "${PORT}"
