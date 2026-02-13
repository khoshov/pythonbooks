# AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Commands

**Run single test:**
```bash
# In Docker
docker compose run -u $(USERID):$(GROUPID) --rm django uv run pytest path/to/test_file.py::test_function_name

# Local
uv run pytest path/to/test_file.py::test_function_name -v
```

**Custom management commands:**
```bash
make books    # Runs parse_books scraper (not python manage.py parse_books)
make tags     # Runs create_default_tags
make assign   # Runs assign_tags_to_books
```

**Docker commands use uv wrapper:**
```bash
# All make commands run through: docker compose run -u $(USERID):$(GROUPID) --rm django uv
# Example: make test → docker compose run ... uv run pytest
```

## Code Style

**Apps location:** Django apps in `apps/` directory, added to sys.path in [`config/settings.py`](config/settings.py:17)

**Import pattern:** Import models/services from apps without `apps.` prefix:
```python
from books.models import Book  # NOT from apps.books.models
```

**Database queries:** Use `.filter().first()` pattern instead of `.get()` to avoid DoesNotExist exceptions (see [`apps/books/services/book_saver.py`](apps/books/services/book_saver.py:59))

**Transactions:** Wrap multi-model operations in `@transaction.atomic` decorator (see [`apps/books/services/book_saver.py`](apps/books/services/book_saver.py:26))

**Scrapers:** All scrapers inherit from [`BaseScraper`](apps/books/scrapers/base_scraper.py) with built-in delay (default 1.0s) and httpx async client

**Logging:** Use custom logger from `logger.books.log` module, not Django's default logger

**Validation:** Use Pydantic models for data validation before saving (see [`apps/books/validators/validators.py`](apps/books/validators/validators.py))

## Testing

**Test location:** Tests in `tests/` directory (not in app directories), configured in [`pytest.ini`](pytest.ini:6)

**Coverage requirement:** 80% minimum coverage enforced by pytest (`--cov-fail-under=80`)

**Database:** Tests use `--reuse-db` flag to speed up test runs

**Markers available:** `slow`, `integration`, `unit`, `api`, `web`, `models`, `services`

## Architecture

**Monorepo structure:**
- Backend: Django REST API (Python 3.11+, Django 4.2.10)
- Frontend: React + TypeScript + Vite (separate `frontend/` directory)
- Services: PostgreSQL, Redis, Celery, Celery Beat, Elasticsearch 7.17

**Service pattern:** Business logic in `apps/books/services/` (author_service, book_saver, publisher_service, tag_matcher)

**Elasticsearch:** Uses django-elasticsearch-dsl 7.4.0 with ES 7.17.0 (not ES 8.x)

**Celery config:** Celery app in [`config/celery_app.py`](config/celery_app.py), tasks in [`apps/books/tasks.py`](apps/books/tasks.py)

**Frontend API:** React app expects Django API on port 8001 (configured in docker-compose.yml), not 8000
