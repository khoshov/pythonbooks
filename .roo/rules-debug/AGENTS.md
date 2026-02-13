# Project Debug Rules (Non-Obvious Only)

## Test Execution
- **Run single test in Docker:**
  ```bash
  docker compose run -u $(USERID):$(GROUPID) --rm django uv run pytest path/to/test_file.py::test_function_name
  ```
- **Tests use `--reuse-db` flag** - database is not recreated between test runs for speed

## Custom Commands
- **Management commands have Makefile shortcuts** (not standard `python manage.py`):
  ```bash
  make books    # Runs parse_books scraper
  make tags     # Runs create_default_tags
  make assign   # Runs assign_tags_to_books
  ```

## Docker Wrapper
- **All make commands run through Docker + uv wrapper:**
  ```bash
  # make test actually runs:
  docker compose run -u $(USERID):$(GROUPID) --rm django uv run pytest
  ```

## Logging
- **Custom logger location:** `logger/books/log.py` (not Django's default logging)
- Scraper logs go to `logs/scrapers/` directory

## Port Configuration
- **Django runs on port 8000 inside container, exposed as 8001 on host** (see docker-compose.yml)
- Frontend expects API on port 8001, not 8000
