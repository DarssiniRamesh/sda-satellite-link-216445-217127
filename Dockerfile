# Lightweight Python base image
FROM python:3.11-slim

WORKDIR /app

# System deps
RUN apt-get update -y && apt-get install -y --no-install-recommends \
    build-essential \
 && rm -rf /var/lib/apt/lists/*

# Copy dependency spec and install
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy source
COPY . /app

# Ensure scripts are executable
RUN chmod +x /app/run.sh /app/bootstrap.sh || true

# Expose default port
ENV PORT=5000
EXPOSE 5000

# Run with uvicorn pointing to root-level main:app (imports ManagementandControlService app)
# Use run.sh to ensure preflight checks (fastapi/uvicorn) in runtime environments
CMD ["sh", "-c", "./run.sh"]
