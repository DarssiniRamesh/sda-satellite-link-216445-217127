#!/usr/bin/env bash
set -euo pipefail

# Navigate to the script directory (service root)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}"

# Install dependencies if not already installed
if [ -f "requirements.txt" ]; then
  pip install --no-input --upgrade pip >/dev/null 2>&1 || true
  pip install --no-input -r requirements.txt
fi

# Export sensible defaults
export PYTHONUNBUFFERED=1

# Start uvicorn with the proper module path and host/port
# This avoids relying on a venv and uses the correct ASGI app import path.
echo "Starting ManagementandControlService on http://0.0.0.0:5000 (ASGI: app.main:app)"
exec uvicorn app.main:app --host 0.0.0.0 --port 5000
