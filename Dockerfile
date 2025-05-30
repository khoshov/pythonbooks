# Use official Python 3.13 slim image based on Debian Bookworm
FROM python:3.13-slim-bookworm

# Install UV (ultra-fast Python package installer) from Astral.sh
COPY --from=ghcr.io/astral-sh/uv:v0.7.4 /uv /uvx /bin/

# Ensure Python output is sent straight to terminal without buffering
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# ======================
# SYSTEM DEPENDENCIES
# ======================
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl gettext && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory inside container
WORKDIR /app

# ======================
# DEPENDENCY INSTALLATION
# ======================
# Copies the dependency files (py project.tool and uv.lock) to /app.
COPY pyproject.toml uv.lock ./

# Install Python dependencies using UV:
# --locked: ensures exact versions from lockfile are used
# Copies the rest of the project code to /app.
RUN uv sync --locked

# ======================
# APPLICATION CODE
# ======================
# Copy the rest of the application code
# Note: This is done after dependency installation for better caching
COPY . .

# Copies the script entrypoint.sh in /app.
# Makes it executable (chmod +x).
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

# ======================
# RUNTIME CONFIGURATION
# ======================
# Expose the port Django runs on
EXPOSE 8000

# Launches the application through a script entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
