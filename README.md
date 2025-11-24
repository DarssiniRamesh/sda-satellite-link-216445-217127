# Project Repository

This repository contains the Management and Control Service (FastAPI) for the SDA Satellite Link project.

## Quick start (local)

1) Create a virtual environment (optional but recommended) and install dependencies:
   python -m venv .venv
   . .venv/bin/activate
   pip install -r requirements.txt

2) Run the service from the repository root:
   uvicorn main:app --host 0.0.0.0 --port 5000

The service exposes:
- GET /health  -> returns {"status": "ok", "service": "..."}
- GET /version -> returns {"version": "...", "environment": "..."}

Environment configuration is read from `.env` if present. Default port is 5000.

## Docker

Build the image:
  docker build -t management-control-service:local .

Run the container:
  docker run --rm -p 5000:5000 --env PORT=5000 management-control-service:local

## Project Structure

- main.py                                      Root entrypoint for uvicorn (main:app)
- ManagementandControlService/__init__.py      Package init, exposes `app`
- ManagementandControlService/app/main.py      FastAPI app with health/version endpoints
- requirements.txt                             Python dependencies
- Dockerfile                                   Container build definition
- .dockerignore                                Docker ignore file
- run.sh                                       Convenience script to run uvicorn

## Notes

- Do not remove or alter existing APIs; this scaffolding is minimal and additive.
- Default PORT is 5000 if not provided.