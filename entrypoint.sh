#!/bin/sh
set -e

uv run python manage.py migrate

if [ "$1" = "celery" ]; then
  shift
  exec uv run celery "$@"
fi

# Transfer control to docker-compose "command"
exec "$@"
