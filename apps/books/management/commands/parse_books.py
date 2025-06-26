import asyncio
from asgiref.sync import sync_to_async
from datetime import datetime
from django.core.management.base import BaseCommand
from urllib.parse import urljoin
from django.db import transaction

from apps.books.models import Book, Author, Publisher
from books.scrapers.piter_publ.book_parser import BookParser
from books.scrapers.piter_publ.piter_scraper import PiterScraper
from books.scrapers.base_scraper import BaseScraper
from logger.logger import setup_logger

logger = setup_logger(module_name=__name__, log_dir="logs/scrapers")


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
        async for link in piter.scrape_book_links(PiterScraper.BASE_URL):
            logger.debug(f"found book link: {link}")
            task = asyncio.create_task(book_scraper.scrape_book(link))
            tasks.append(task)

        for coro in asyncio.as_completed(tasks):
            book = await coro
            if book:
                await self.save_book(book)

    async def save_book(self, item: dict):
        await sync_to_async(self._save_book_sync)(item)

    @transaction.atomic
    def _save_book_sync(self, item: dict):
        authors_data = item["author"]
        details = item["details"]
        isbn = details.get("ISBN", "").strip()

        if not isbn:
            logger.warning(f"skipped book without ISBN: {item['book_title']}")
            return

        raw_year = details.get("Год", "2024")
        try:
            published_at = datetime.strptime(raw_year, "%Y").date()
        except ValueError:
            published_at = datetime.strptime("2024", "%Y").date()

        publisher, _ = Publisher.objects.get_or_create(name="Издательство Питер")

        book = Book.objects.filter(isbn_code=isbn).first()
        if book:
            logger.info(f"updating book: {book.title} ({isbn})")
            book.title = item["book_title"]
            book.description = item["description"]
            book.published_at = published_at
            book.total_pages = int(details.get("Страниц", 0))
            book.cover_image = item["cover"].get("cover_image", "")
            book.language = "Русский"
            book.publisher = publisher
            book.save()
        else:
            logger.info(f"creating new book: {item['book_title']} ({isbn})")
            book = Book.objects.create(
                isbn_code=isbn,
                title=item["book_title"],
                description=item["description"],
                published_at=published_at,
                total_pages=int(details.get("Страниц", 0)),
                cover_image=item["cover"].get("cover_image", ""),
                language="Русский",
                publisher=publisher,
            )

        authors = []
        for author_data in authors_data:
            first_name = author_data.get("first_name", "").strip()
            last_name = author_data.get("last_name", "").strip()
            bio = author_data.get("bio", "").strip()
            if not first_name and not last_name:
                continue
            author_obj, _ = Author.objects.get_or_create(
                first_name=first_name,
                last_name=last_name,
                bio=bio,
            )
            authors.append(author_obj)

        book.author.set(authors)
        logger.debug(f"saved book with authors: {item['book_title']}")
