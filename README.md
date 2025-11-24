# Project Repository

This is the initial README file for the project.

## ManagementandControlService

- App entrypoint: `sda-satellite-link-216445-217127/ManagementandControlService/app/main.py`
- Uvicorn start command: `uvicorn app.main:app --host 0.0.0.0 --port 5000` (preferred)
- ASGI import shim is available, so `uvicorn main:app --host 0.0.0.0 --port 5000` also works
- Health endpoint: `GET /health` returns `{ "status": "ok", "service": "ManagementandControlService", "version": "0.1.0" }`

Quick start:
1. Change directory to the service:
   ```
   cd sda-satellite-link-216445-217127/ManagementandControlService
   ```
2. Run the service:
   ```
   ./run.sh
   ```
3. Open API docs at http://localhost:5000/docs