#!/usr/bin/env sh
set -e

PORT="${PORT:-5000}"
HOST="${HOST:-0.0.0.0}"

echo "Starting ManagementandControlService on ${HOST}:${PORT}"
exec uvicorn main:app --host "${HOST}" --port "${PORT}"
