#!/usr/bin/env sh
# Robust runner: ensures venv exists/activated, installs requirements, preflight checks FastAPI/uvicorn, then starts server.
set -e

PORT="${PORT:-5000}"
HOST="${HOST:-0.0.0.0}"

# 1) Ensure we are in repo root (contains requirements.txt and main.py)
SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
cd "$SCRIPT_DIR"

# 2) Create/activate venv if none active
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

# 3) Preflight import check; if fails, install/repair and re-check
preflight_check() {
  python - <<'PYCODE'
try:
    import fastapi  # noqa: F401
    import uvicorn  # noqa: F401
    print("Preflight OK: fastapi and uvicorn are importable")
except Exception as e:
    raise SystemExit(f"Preflight import failed: {e}")
PYCODE
}

echo "Running preflight import check..."
if ! preflight_check; then
  echo "Preflight failed, attempting to install requirements..."
  if [ -f "requirements.txt" ]; then
    python -m pip install --upgrade pip >/dev/null 2>&1 || true
    python -m pip install --no-cache-dir -r requirements.txt
  else
    echo "ERROR: requirements.txt not found in $(pwd)."
  fi
  echo "Re-running preflight import check..."
  preflight_check
else
  echo "Preflight passed."
fi

# 4) Ensure dependencies are installed (idempotent)
if [ -f "requirements.txt" ]; then
  echo "Ensuring Python dependencies are installed from requirements.txt ..."
  python -m pip install --no-cache-dir -r requirements.txt >/dev/null 2>&1 || true
fi

echo "Starting ManagementandControlService on ${HOST}:${PORT}"
# Use repo-root main:app which imports ManagementandControlService.app.main
exec uvicorn main:app --host "${HOST}" --port "${PORT}"
