FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose Render's web-service port
EXPOSE 8000

# Health check
HEALTHCHECK CMD curl --fail http://localhost:${PORT:-8000}/health || exit 1

# Run the FastAPI backend. Render supplies PORT at runtime.
CMD uvicorn backend_api:app --host 0.0.0.0 --port ${PORT:-8000}
