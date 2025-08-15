import pytest
import asyncio
from unittest.mock import Mock

from apps.books.management.commands.parse_books import Command, AsyncBookFetcher
from apps.books.scrapers.piter_publ.piter_scraper import PiterScraper


class TestCommand:
    """тесты для Command класса"""

    def test_command_init(self):
        """тест инициализации команды"""
        cmd = Command()
        assert cmd.help == "Парсит книги с сайта Piter и сохраняет в базу данных"

    def test_command_handle(self, monkeypatch):
        """тест метода handle"""
        asyncio_run_called = False

        def fake_run(coro):
            nonlocal asyncio_run_called
            asyncio_run_called = True
            if hasattr(coro, "close"):
                coro.close()

        monkeypatch.setattr(asyncio, "run", fake_run)

        logger_mock = Mock()
        monkeypatch.setattr(
            "apps.books.management.commands.parse_books.logger", logger_mock
        )

        cmd = Command()
        cmd.handle()

        assert asyncio_run_called
        assert logger_mock.info.call_count == 2

    @pytest.mark.asyncio
    async def test_import_books_integration(self, monkeypatch):
        """тест основного процесса импорта"""

        async def fake_scrape_book_links(self):
            yield "/collection/all/product/test1"
            yield "/collection/all/product/test2"

        async def fake_scrape_book(self, url):
            return {
                "url": url,
                "book_title": f"Book from {url}",
                "author": [],
                "price": {},
                "details": {},
                "description": "",
                "cover": {},
            }

        saved_books = []

        async def fake_save_book(self, book_data):
            saved_books.append(book_data)

        monkeypatch.setattr(PiterScraper, "scrape_book_links", fake_scrape_book_links)
        monkeypatch.setattr(AsyncBookFetcher, "scrape_book", fake_scrape_book)
        monkeypatch.setattr(Command, "save_book", fake_save_book)

        cmd = Command()
        await cmd.import_books()

        assert len(saved_books) == 2

    @pytest.mark.asyncio
    async def test_import_books_skips_none(self, monkeypatch):
        """тест пропуска None результатов"""

        async def fake_scrape_book_links(self):
            yield "/collection/all/product/test1"
            yield "/collection/all/product/test2"

        call_count = 0

        async def fake_scrape_book(self, url):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return None
            return {"url": url, "book_title": "Valid Book"}

        saved_books = []

        async def fake_save_book(self, book_data):
            saved_books.append(book_data)

        monkeypatch.setattr(PiterScraper, "scrape_book_links", fake_scrape_book_links)
        monkeypatch.setattr(AsyncBookFetcher, "scrape_book", fake_scrape_book)
        monkeypatch.setattr(Command, "save_book", fake_save_book)

        cmd = Command()
        await cmd.import_books()

        assert len(saved_books) == 1

    @pytest.mark.asyncio
    async def test_save_book_method(self, monkeypatch):
        """тест метода save_book"""
        sync_to_async_mock = Mock()

        async def fake_async_function(*args, **kwargs):
            return None

        sync_to_async_mock.return_value = fake_async_function
        monkeypatch.setattr(
            "apps.books.management.commands.parse_books.sync_to_async",
            sync_to_async_mock,
        )

        cmd = Command()
        test_item = {"title": "Test Book"}

        await cmd.save_book(test_item)

        assert sync_to_async_mock.called


class TestAsyncBookFetcher:
    """Тесты для AsyncBookFetcher класса"""

    def test_async_book_fetcher_init(self):
        """тест инициализации AsyncBookFetcher"""
        fetcher = AsyncBookFetcher(
            base_domain="https://test.com", delay=1.5, max_concurrent=5
        )

        assert fetcher.base_domain == "https://test.com"
        assert fetcher.delay == 1.5
        assert fetcher.semaphore._value == 5
        assert fetcher._last_request_time == 0

    @pytest.mark.asyncio
    async def test_scrape_book_success(self, monkeypatch):
        """тест успешного парсинга книги"""
        fetcher = AsyncBookFetcher("https://test.com", delay=0)

        fake_html = """
        <div class="product-info"><h1>Test Book Title</h1></div>
        <div id="tab-1">Test book description</div>
        """

        async def fake_fetch(self, url):
            return fake_html

        logger_mock = Mock()
        monkeypatch.setattr(
            "apps.books.management.commands.parse_books.logger", logger_mock
        )
        monkeypatch.setattr(AsyncBookFetcher, "fetch", fake_fetch)

        result = await fetcher.scrape_book("https://test.com/book/123")

        assert result is not None
        assert result["url"] == "https://test.com/book/123"
        assert result["book_title"] == "Test Book Title"
        assert result["description"] == "Test book description"

    @pytest.mark.asyncio
    async def test_scrape_book_fetch_failed(self, monkeypatch):
        """тест когда fetch возвращает None"""
        fetcher = AsyncBookFetcher("https://test.com", delay=0)

        async def fake_fetch_none(self, url):
            return None

        logger_mock = Mock()
        monkeypatch.setattr(
            "apps.books.management.commands.parse_books.logger", logger_mock
        )
        monkeypatch.setattr(AsyncBookFetcher, "fetch", fake_fetch_none)

        result = await fetcher.scrape_book("https://test.com/book/123")

        assert result is None
        logger_mock.warning.assert_called_with(
            "failed to fetch https://test.com/book/123"
        )
