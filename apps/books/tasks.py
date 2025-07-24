import asyncio

from asgiref.sync import sync_to_async
from celery import shared_task

from .management.commands.parse_books import (
    AsyncBookFetcher,
    book_saver,
    logger,
)
from .scrapers.piter_publ.piter_scraper import PiterScraper


@shared_task
def parse_books_task():
    """
    celery-задача для запуска парсинга книг
    """

    async def import_books():
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
                await sync_to_async(book_saver.save_book)(book)

    asyncio.run(import_books())
