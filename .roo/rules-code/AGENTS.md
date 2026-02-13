# Project Coding Rules (Non-Obvious Only)

## Import Patterns
- Apps in `apps/` directory are added to sys.path - import without `apps.` prefix:
  ```python
  from books.models import Book  # NOT from apps.books.models
  from books.services.book_saver import BookSaver  # NOT from apps.books...
  ```

## Database Patterns
- **Always use `.filter().first()` instead of `.get()`** to avoid DoesNotExist exceptions
  ```python
  book = Book.objects.filter(isbn_code=isbn).first()  # Returns None if not found
  # NOT: book = Book.objects.get(isbn_code=isbn)  # Raises exception
  ```

- **Wrap multi-model operations in `@transaction.atomic`** (see [`apps/books/services/book_saver.py`](../../apps/books/services/book_saver.py:26))
  ```python
  from django.db import transaction
  
  @transaction.atomic
  def save_book(self, item: dict):
      # Multiple DB operations here
  ```

## Custom Utilities
- **Scrapers must inherit from [`BaseScraper`](../../apps/books/scrapers/base_scraper.py)** - provides built-in delay (default 1.0s) and httpx async client
- **Use custom logger from `logger.books.log`**, not Django's default logger:
  ```python
  from logger.books.log import get_logger
  logger = get_logger(__name__)
  ```

## Validation
- **Use Pydantic models for data validation** before saving to database (see [`apps/books/validators/validators.py`](../../apps/books/validators/validators.py))

## Service Layer
- Business logic goes in `apps/books/services/` directory, not in views or models
- Services: `author_service`, `book_saver`, `publisher_service`, `tag_matcher`
