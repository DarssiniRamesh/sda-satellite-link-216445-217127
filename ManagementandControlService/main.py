"""ASGI entrypoint for ManagementandControlService.

This module re-exports the FastAPI `app` from src.api.main so that running:
    uvicorn main:app
from the container root works seamlessly with the preview orchestrator.

No configuration is hardcoded here; configuration should be provided via environment
variables consumed by src.api.settings.get_settings().

Security notes:
- This file only re-exports the application object; no external inputs are handled here.
- Ports and hosts are controlled by uvicorn invocation and orchestration, not in code.
"""

from __future__ import annotations

# PUBLIC_INTERFACE
# Re-export FastAPI application instance for ASGI servers.
# Usage:
#   uvicorn main:app --host 0.0.0.0 --port "${PORT:-8000}"
from src.api.main import app  # noqa: F401  (re-exported symbol)
