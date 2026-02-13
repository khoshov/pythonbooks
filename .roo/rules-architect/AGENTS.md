# Project Architecture Rules (Non-Obvious Only)

## Service Layer Pattern
- **Business logic must go in `apps/books/services/`**, not in views or models
- Services are stateless and handle complex operations:
  - `book_saver.py` - Orchestrates book creation with validation, author/publisher linking
  - `author_service.py` - Author CRUD with get_or_create pattern
  - `publisher_service.py` - Publisher management
  - `tag_matcher.py` - Tag matching algorithm

## Data Flow
1. Scrapers (inherit from [`BaseScraper`](../../apps/books/scrapers/base_scraper.py)) → 
2. Pydantic validation ([`validators.py`](../../apps/books/validators/validators.py)) → 
3. Service layer (`apps/books/services/`) → 
4. Django ORM models

## Transaction Boundaries
- **Multi-model operations wrapped in `@transaction.atomic`** (see [`book_saver.py`](../../apps/books/services/book_saver.py:26))
- Ensures atomicity when creating/updating books with related authors and publishers

## Scraper Architecture
- All scrapers inherit from `BaseScraper` with:
  - Built-in delay (default 1.0s) to avoid rate limiting
  - httpx async client for concurrent requests
  - BeautifulSoup parser wrapper

## Validation Layer
- **Pydantic models validate data before database operations**
- Prevents invalid data from reaching Django ORM
- Located in `apps/books/validators/validators.py`

## Logging Architecture
- **Custom logger in `logger/books/log.py`** (not Django's default)
- Scraper logs stored in `logs/scrapers/` directory
- Services use custom logger for consistent formatting

## Elasticsearch Integration
- **ES 7.17.0 only** (not compatible with ES 8.x)
- Documents defined in `apps/books/documents.py`
- Uses django-elasticsearch-dsl 7.4.0

## Celery Task Architecture
- Celery app in [`config/celery_app.py`](../../config/celery_app.py)
- Tasks in [`apps/books/tasks.py`](../../apps/books/tasks.py)
- Celery Beat for scheduled tasks (periodic scraping)

## Frontend-Backend Separation
- **Frontend expects API on port 8001** (docker-compose maps 8000→8001)
- CORS configured for React dev server (port 5173)
- API versioned under `/api/v1/`
