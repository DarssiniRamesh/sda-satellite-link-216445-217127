# ManagementandControlService

Minimal FastAPI scaffolding providing health and root endpoints.

## Endpoints
- GET `/` — service metadata
- GET `/health` — health probe

## Run locally
```bash
pip install -r requirements.txt

# Option A: Run via root-level ASGI entrypoint (preferred for orchestrator)
uvicorn main:app --host 0.0.0.0 --port "${PORT:-8000}"

# Option B: Run via module path
uvicorn src.api.main:app --host 0.0.0.0 --port "${PORT:-8000}"
```
