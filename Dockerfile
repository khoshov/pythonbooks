# Use official Python 3.13 slim image based on Debian Bookworm
FROM python:3.13-slim-bookworm

# Install UV (ultra-fast Python package installer) from Astral.sh
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Ensure Python output is sent straight to terminal without buffering
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_SYSTEM_PYTHON=1

# ======================
# SYSTEM DEPENDENCIES
# ======================
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        curl \
        gettext \
        ca-certificates && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /tmp/* /var/tmp/*

# Set working directory inside container
WORKDIR /app

# ======================
# DEPENDENCY INSTALLATION
# ======================
# Copy dependency files with proper ownership
COPY --chown=appuser:appuser pyproject.toml uv.lock ./

# Install Python dependencies using UV
RUN uv sync --locked --no-dev

# ======================
# APPLICATION CODE
# ======================
# Copy entrypoint script first
COPY --chown=appuser:appuser entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# Copy the rest of the application code
COPY --chown=appuser:appuser . .

# Create directories for Django with proper permissions
RUN mkdir -p /app/static /app/media && \
    chown -R appuser:appuser /app

# ======================
# RUNTIME CONFIGURATION
# ======================
# Switch to non-root user
USER appuser

# Expose the port Django runs on
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

# Launches the application through a script entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
