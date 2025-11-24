# SDA Satellite Link - Services

This repository contains multiple FastAPI backend services for the SDA Satellite Link project.

## Management and Control Service

Location:
- sda-satellite-link-216445-217127/ManagementandControlService

Entry point:
- Top-level ASGI module: main.py exporting `app`
- Start command: `uvicorn main:app --host 0.0.0.0 --port 3000`

Environment:
- Copy `.env.example` to `.env` and adjust as needed.
- Supported ports: 3000, 3001, 3002, 5000. Default: 3000.

Example:
```
cd sda-satellite-link-216445-217127/ManagementandControlService
cp .env.example .env
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 3000
```

Health and Swagger:
- Liveness: http://localhost:3000/
- Readiness: http://localhost:3000/health
- Docs: http://localhost:3000/docs
- OpenAPI: http://localhost:3000/openapi.json

Preview environment:
- The preview platform may bind the service to port 3010. This service now honors any valid PORT value.
- Example for preview: `export PORT=3010 && uvicorn main:app --host 0.0.0.0 --port \"$PORT\"`

## Notes

- Defaults remain: Management=3000, DataPlane=3002, Protocol=5000. Any valid PORT is accepted.
- Do not hardcode secrets or credentials in code. Use environment variables via `.env`.
