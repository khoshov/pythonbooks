# Project Documentation Rules (Non-Obvious Only)

## Project Structure
- **Apps in `apps/` directory** - added to sys.path in [`config/settings.py`](../../config/settings.py:17), so imports don't need `apps.` prefix
- **Tests in `tests/` directory** (not in app directories) - configured in [`pytest.ini`](../../pytest.ini:6)
- **Frontend is separate React app** in `frontend/` directory with own package.json

## Monorepo Architecture
- Backend: Django REST API (Python 3.11+, Django 4.2.10)
- Frontend: React + TypeScript + Vite
- Services: PostgreSQL, Redis, Celery, Celery Beat, Elasticsearch 7.17

## Version Constraints
- **Elasticsearch 7.17.0** (not ES 8.x) - uses django-elasticsearch-dsl 7.4.0
- **Django 4.2.10** - pinned for ES 7 compatibility

## Service Layer Pattern
- Business logic in `apps/books/services/` directory:
  - `author_service.py` - Author CRUD operations
  - `book_saver.py` - Book saving with validation
  - `publisher_service.py` - Publisher operations
  - `tag_matcher.py` - Tag matching logic

## Custom Management Commands
- Located in `apps/books/management/commands/`:
  - `parse_books.py` - Book scraper
  - `create_default_tags.py` - Tag initialization
  - `assign_tags_to_books.py` - Tag assignment

## Port Configuration
- Django API runs on port 8001 (not 8000) when using docker-compose
- Frontend dev server on port 5173 (Vite default)
