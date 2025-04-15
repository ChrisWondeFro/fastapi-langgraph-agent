FROM python:3.12.2-slim

# Set working directory
WORKDIR /app

# Set non-sensitive environment variables
ARG APP_ENV=development
ARG POSTGRES_URL

ENV APP_ENV=${APP_ENV} \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POSTGRES_URL=${POSTGRES_URL}

# Install system dependencies and pip/uv
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && pip install --upgrade pip \
    && pip install uv \
    && rm -rf /var/lib/apt/lists/*

# Copy in only what's needed to install deps first to leverage Docker cache
COPY pyproject.toml uv.lock README.md ./

# Create virtual environment and install dependencies in editable mode
RUN uv venv && . .venv/bin/activate && uv pip install -e .

# Copy full app (after installing deps to cache layers)
COPY . .

# Create log directory early for smoother volume mapping if needed
RUN mkdir -p /app/logs

# Make entrypoint script executable
RUN chmod +x /app/scripts/docker-entrypoint.sh

# Create non-root user and assign permissions
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose default app port
EXPOSE 8000

# Log environment at build time (not runtime)
RUN echo "Using ${APP_ENV} environment"

# Default entrypoint and command
ENTRYPOINT ["/app/scripts/docker-entrypoint.sh"]
CMD ["/app/.venv/bin/uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]