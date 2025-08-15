import asyncio
from urllib.parse import urljoin

from asgiref.sync import sync_to_async
from django.core.management.base import BaseCommand

from apps.books.models import Author, Book, Publisher
from apps.books.scrapers.base_scraper import BaseScraper
from apps.books.scrapers.piter_publ.book_parser import BookParser
from apps.books.scrapers.piter_publ.piter_scraper import PiterScraper
from apps.books.services.author_service import AuthorService
from apps.books.services.book_saver import BookSaver
from apps.books.services.publisher_service import PublisherService
from logger.books.log import get_logger

logger = get_logger(__name__)
author_service = AuthorService(Author)
publisher_service = PublisherService(Publisher)
book_saver = BookSaver(Book, publisher_service, author_service, logger)


class AsyncBookFetcher(BaseScraper):
    def __init__(self, base_domain: str, delay: float = 2.0, max_concurrent: int = 3):
        super().__init__(delay)
        self.base_domain = base_domain
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self._last_request_time = 0

    async def scrape_book(self, url: str):
        async with self.semaphore:
            now = asyncio.get_event_loop().time()
            elapsed = now - self._last_request_time
            if elapsed < self.delay:
                await asyncio.sleep(self.delay - elapsed)
            self._last_request_time = asyncio.get_event_loop().time()

            if url.startswith("/"):
                url = urljoin(self.base_domain, url)

            logger.info(f"fetching book: {url}")
            html = await self.fetch(url)
            if not html:
                logger.warning(f"failed to fetch {url}")
                return None

            parser = BookParser(html)
            book_data = {
                "url": url,
                "book_title": parser.extract_book_name().get("book_title", ""),
                "author": parser.extract_authors(),
                "price": parser.extract_price(),
                "details": parser.extract_all_params(),
                "description": parser.extract_description().get("description", ""),
                "cover": parser.extract_cover_image(),
            }
            logger.debug(f"parsed book data for: {book_data['book_title']}")
            return book_data


class Command(BaseCommand):
    help = "Парсит книги с сайта Piter и сохраняет в базу данных"

    def handle(self, *args, **kwargs):
        logger.info("starting book import from Piter")
        asyncio.run(self.import_books())
        logger.info("book import finished")

    async def import_books(self):
        piter = PiterScraper()
        book_scraper = AsyncBookFetcher(base_domain="https://www.piter.com")

        tasks = []
        async for link in piter.scrape_book_links():
            logger.debug(f"found book link: {link}")
            task = asyncio.create_task(book_scraper.scrape_book(link))
            tasks.append(task)

        for coro in asyncio.as_completed(tasks):
            book = await coro
            if book:
                await self.save_book(book)

    async def save_book(self, item: dict):
        await sync_to_async(book_saver.save_book)(item)
