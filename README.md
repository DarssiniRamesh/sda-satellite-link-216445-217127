# SDA Satellite Link - Services

This repository contains multiple FastAPI backend services for the SDA Satellite Link project.

## Management and Control Service

Location:
- sda-satellite-link-216445-217127/ManagementandControlService

Entry point:
- Top-level ASGI module: main.py exporting `app`
- Start command (preview/CI): `uvicorn main:app --host 0.0.0.0 --port $PORT`

Environment:
- Copy `.env.example` to `.env` and adjust as needed.
- Supported ports: 3000, 3001, 3002, 5000. If `PORT` is not set, defaults to 3000.

Example:
```
cd sda-satellite-link-216445-217127/ManagementandControlService
cp .env.example .env
# optionally edit .env to set PORT
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port ${PORT:-3000}
```

Health check:
- GET `http://localhost:${PORT:-3000}/` returns `{ "message": "Healthy" }`.

## Notes

- Ports are standardized across containers to: 3000, 3001, 3002, 5000.
- Do not hardcode secrets or credentials in code. Use environment variables via `.env`.
