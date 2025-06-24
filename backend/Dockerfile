FROM python:3.11-slim

LABEL name="simsynai-backend" \
      version="1.0.0" \
      description="SimSynAI Backend Service"

WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PIP_DEFAULT_TIMEOUT=600 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install curl for health checks and configure pip
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip config set global.index-url https://mirrors.aliyun.com/pypi/simple/ && \
    pip config set global.timeout 600 && \
    pip config set global.trusted-host mirrors.aliyun.com

# Install dependencies in batches to avoid timeout issues
COPY requirements.txt .
RUN pip install --no-cache-dir pip -U && \
    # Core dependencies first
    pip install --no-cache-dir fastapi uvicorn python-multipart email-validator && \
    # Database dependencies
    pip install --no-cache-dir sqlalchemy alembic pydantic pydantic-settings && \
    # Auth dependencies
    pip install --no-cache-dir python-jose passlib bcrypt && \
    # AI dependencies
    pip install --no-cache-dir openai anthropic httpx && \
    # Data science dependencies
    pip install --no-cache-dir numpy pandas && \
    # Remaining dependencies
    pip install --no-cache-dir -r requirements.txt || echo "Some packages may not have been installed"

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p logs simulation_results

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl --fail http://localhost:8000/api/v1/health || exit 1

# Start command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 