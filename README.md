# Project Repository

This is the initial README file for the project.

## ManagementandControlService

- App entrypoint: `sda-satellite-link-216445-217127/ManagementandControlService/app/main.py`
- Default service port: 5000
- Uvicorn start command (preferred): `uvicorn app.main:app --host 0.0.0.0 --port 5000`
- ASGI import shim is available, so `uvicorn main:app --host 0.0.0.0 --port 5000` also works
- Health endpoint: `GET /health` returns `{ "status": "ok", "service": "ManagementandControlService", "version": "0.1.0" }`

### Port configuration (environment override)
This service binds to port 5000 by default. You can override the port by setting the `PORT` environment variable.

Examples:
- One-off run: `PORT=5050 ./run.sh` will bind to `http://0.0.0.0:5050`
- Using a `.env` file: copy `.env.example` to `.env` and adjust `PORT`.

Optional host override is supported via `HOST` (defaults to `0.0.0.0`).

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