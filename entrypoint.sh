#!/bin/sh
set -e

uv run python manage.py migrate

# Transfer control to docker-compose "command"
exec "$@"
