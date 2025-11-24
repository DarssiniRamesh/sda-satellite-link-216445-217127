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
- Health: http://localhost:3000/
- Docs: http://localhost:3000/docs

## Notes

- Ports are standardized across containers to: 3000, 3001, 3002, 5000.
- Do not hardcode secrets or credentials in code. Use environment variables via `.env`.
