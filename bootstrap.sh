#!/usr/bin/env sh
# PUBLIC_INTERFACE
# Bootstrap script: creates/activates a virtualenv, installs dependencies,
# validates FastAPI import, and starts uvicorn main:app.
# Usage:
#   ./bootstrap.sh
#   PORT=8000 HOST=127.0.0.1 ./bootstrap.sh
# Notes:
# - Respects existing activated venv; only creates .venv if none active.
# - Uses PORT env var with default 5000.

set -e

PORT="${PORT:-5000}"
HOST="${HOST:-0.0.0.0}"

# Create venv if none is active
if [ -z "${VIRTUAL_ENV:-}" ]; then
  if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment at ./.venv ..."
    python -m venv .venv
  fi
  # shellcheck disable=SC1091
  . .venv/bin/activate
  echo "Activated virtual environment: ${VIRTUAL_ENV}"
else
  echo "Using existing virtual environment: ${VIRTUAL_ENV}"
fi

# Upgrade pip and install deps
if [ -f "requirements.txt" ]; then
  echo "Installing Python dependencies from requirements.txt..."
  python -m pip install --upgrade pip >/dev/null 2>&1 || true
  python -m pip install --no-cache-dir -r requirements.txt
else
  echo "requirements.txt not found in $(pwd)."
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
# Ensure working directory remains project root so 'main:app' resolves
exec uvicorn main:app --host "${HOST}" --port "${PORT}"
