# Project Repository

This repository contains the Management and Control Service (FastAPI) for the SDA Satellite Link project.

## Quick start (local)

Option A: Use bootstrap.sh (creates venv, installs deps, starts server)
  ./bootstrap.sh
  PORT=8000 HOST=127.0.0.1 ./bootstrap.sh

Option B: Manual setup
1) Create a virtual environment (optional but recommended) and install dependencies:
   python -m venv .venv
   . .venv/bin/activate
   pip install -r requirements.txt

2) Run the service from the repository root:
   uvicorn main:app --host 0.0.0.0 --port ${PORT:-5000}

The service exposes:
- GET /health  -> returns {"status": "ok", "service": "..."}
- GET /version -> returns {"version": "...", "environment": "..."}

Environment configuration is read from `.env` if present. Default port is 5000.
The uvicorn entrypoint is main:app and requires the working directory to be the repo root
so main.py can import ManagementandControlService.app.main.

## Docker

Build the image:
  docker build -t management-control-service:local .

Run the container:
  docker run --rm -p 5000:5000 --env PORT=5000 management-control-service:local

## Project Structure

- main.py                                      Root entrypoint for uvicorn (main:app)
- ManagementandControlService/__init__.py      Package init, exposes `app`
- ManagementandControlService/app/main.py      FastAPI app with health/version endpoints
- requirements.txt                             Python dependencies (fastapi, uvicorn, pydantic, pydantic-settings, python-dotenv)
- Dockerfile                                   Container build definition
- .dockerignore                                Docker ignore file
- run.sh                                       Convenience script to run uvicorn locally
- bootstrap.sh                                 Creates venv, installs deps, starts uvicorn

## Notes

- Do not remove or alter existing APIs; this scaffolding is minimal and additive.
- Default PORT is 5000 if not provided (set PORT env var to override).